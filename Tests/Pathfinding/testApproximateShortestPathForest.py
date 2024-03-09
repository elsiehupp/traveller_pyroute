"""
Created on Feb 19, 2024

@author: CyberiaResurrection
"""
import argparse
import copy
import json
import os
import tempfile
import unittest

import networkx as nx
import numpy as np

from PyRoute.Pathfinding.LandmarkSchemes.LandmarksTriaxialExtremes import LandmarksTriaxialExtremes
from PyRoute.Pathfinding.LandmarkSchemes.LandmarksWTNExtremes import LandmarksWTNExtremes
from PyRoute.DeltaDebug.DeltaDictionary import SectorDictionary, DeltaDictionary
from PyRoute.DeltaDebug.DeltaGalaxy import DeltaGalaxy
from PyRoute.Pathfinding.ApproximateShortestPathForestDistanceGraph import ApproximateShortestPathForestDistanceGraph
from PyRoute.Pathfinding.ApproximateShortestPathForestUnified import ApproximateShortestPathForestUnified
from Tests.baseTest import baseTest


class testApproximateShortestPathForest(baseTest):
    def test_triaxial_bounds_should_wrap_three_trees(self):
        galaxy = self.set_up_zarushagar_sector()

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks = foo.get_landmarks(index=True)
        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]

        approx = ApproximateShortestPathForestDistanceGraph(source, graph, 0.2, sources=landmarks)
        self.assertEqual(3, len(approx._trees), "Unexpected number of approx-SP trees")

        src = stars[2]
        targ = stars[80]

        expected = 310.833
        actual = approx.lower_bound(src, targ)
        self.assertAlmostEqual(expected, actual, 3, "Unexpected lower bound value")

        approx = ApproximateShortestPathForestDistanceGraph(source, graph, 0.2, sources=landmarks)
        self.assertEqual(3, len(approx._trees), "Unexpected number of approx-SP trees")

        src = stars[2]
        targ = stars[80]

        expected = 310.833
        actual = approx.lower_bound(src, targ)
        self.assertAlmostEqual(expected, actual, 3, "Unexpected lower bound value")

    def test_trixial_bounds_in_bulk(self):
        galaxy = self.set_up_zarushagar_sector()

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks = foo.get_landmarks(index=True)
        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]

        approx = ApproximateShortestPathForestDistanceGraph(source, graph, 0.2, sources=landmarks)

        active_nodes = [2, 80]
        target = 80
        expected = np.array([310.833, 0])
        actual = approx.lower_bound_bulk(active_nodes, target)
        self.assertIsNotNone(actual)

        np.testing.assert_array_almost_equal(expected, actual, 0.000001, "Unexpected bounds array")

    def test_trixial_bounds_in_bulk_unified(self):
        galaxy = self.set_up_zarushagar_sector()

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks = foo.get_landmarks(index=True)
        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]

        approx = ApproximateShortestPathForestUnified(source, graph, 0.2, sources=landmarks)
        self.assertEqual(3, approx._num_trees)

        active_nodes = [2, 80]
        target = 80
        expected = np.array([310.833, 0])
        actual = approx.lower_bound_bulk(active_nodes, target)
        self.assertIsNotNone(actual)

        np.testing.assert_array_almost_equal(expected, actual, 0.000001, "Unexpected bounds array")

    def test_unified_can_handle_singleton_landmarks(self):
        galaxy = self.set_up_zarushagar_sector()

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks = foo.get_landmarks(index=True)[0]
        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]

        approx = ApproximateShortestPathForestUnified(source, graph, 0.2, sources=landmarks)
        self.assertEqual(1, approx._num_trees)

    def test_unified_can_handle_bulk_lobound_from_singleton_component(self):
        galaxy = self.set_up_zarushagar_sector()

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks = foo.get_landmarks(index=True)
        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]
        targ = [item for item in graph if graph.nodes()[item]['star'].component == 1][0]

        approx = ApproximateShortestPathForestUnified(source, graph, 0.2, sources=landmarks)

        bulk_lo = approx.lower_bound_bulk(stars, targ)
        self.assertEqual(1129.1666666666667, max(bulk_lo), "Unexpected lobound")

    def test_unified_can_handle_bulk_lobound_to_singleton_component(self):
        galaxy = self.set_up_zarushagar_sector()

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks = foo.get_landmarks(index=True)
        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]
        targ = [item for item in graph if graph.nodes()[item]['star'].component == 1][0]

        approx = ApproximateShortestPathForestUnified(source, graph, 0.2, sources=landmarks)

        bulk_lo = approx.lower_bound_bulk(stars, source)
        self.assertEqual(float('+inf'), bulk_lo[targ])

    def test_verify_near_root_edge_propagates(self):
        sourcefile = self.unpack_filename('DeltaFiles/Zarushagar-Ibara.sec')
        jsonfile = self.unpack_filename('PathfindingFiles/single_source_distances_ibara_subsector_from_0101.json')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, 1, False)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        graph = galaxy.stars
        stars = list(graph.nodes)
        source = stars[0]
        leafnode = stars[30]

        approx = ApproximateShortestPathForestUnified(source, graph, 0)

        # auxiliary network dijkstra calculation to dish out parent nodes
        paths = nx.single_source_dijkstra_path(graph, source)
        right = paths[leafnode][1]

        # seed expected distances
        with open(jsonfile, 'r') as file:
            expected_string = json.load(file)

        expected_distances = dict()
        component = [item for item in stars if graph.nodes[item]['star'].component == graph.nodes[source]['star'].component]
        for item in component:
            exp_dist = 0
            rawstar = graph.nodes[item]['star']
            if str(rawstar) in expected_string:
                exp_dist = expected_string[str(rawstar)]
            expected_distances[item] = exp_dist

        distance_check = list(expected_distances.values()) == approx._distances[:,0]
        self.assertTrue(distance_check.all(), "Unexpected distances after SPT creation")

        # adjust weight
        oldweight = galaxy.stars[source][right]['weight']
        galaxy.stars[source][right]['weight'] -= 1
        galaxy.trade.star_graph.lighten_edge(source, right, oldweight - 1)
        approx._graph.lighten_edge(source, right, oldweight - 1)

        # tell SPT weight has changed
        edge = (source, right)

        for item in expected_distances:
            if expected_distances[item] > 0 and 'Selsinia (Zarushagar 0201)' != str(graph.nodes[item]['star']):
                expected_distances[item] -= 1

        approx.update_edges([edge])

        distance_check = list(expected_distances.values()) == approx._distances[:, 0]
        self.assertTrue(distance_check.all(), "Unexpected distances after SPT restart")

    def set_up_zarushagar_sector(self):
        sourcefile = self.unpack_filename('DeltaFiles/Zarushagar.sec')
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector
        args = self._make_args()
        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output
        galaxy.generate_routes()
        galaxy.trade.calculate_components()
        return galaxy


if __name__ == '__main__':
    unittest.main()
