"""
Created on Feb 19, 2024

@author: CyberiaResurrection
"""
from collections import defaultdict

from PyRoute.DeltaDebug.DeltaGalaxy import DeltaGalaxy
from PyRoute.DeltaDebug.DeltaDictionary import SectorDictionary, DeltaDictionary
from PyRoute.Pathfinding.DistanceGraph import DistanceGraph
from PyRoute.Pathfinding.LandmarkSchemes.LandmarksQExtremes import LandmarksQExtremes
from PyRoute.Pathfinding.LandmarkSchemes.LandmarksRExtremes import LandmarksRExtremes
from PyRoute.Pathfinding.LandmarkSchemes.LandmarksSExtremes import LandmarksSExtremes
from PyRoute.Pathfinding.LandmarkSchemes.LandmarksTriaxialExtremes import LandmarksTriaxialExtremes
from PyRoute.Inputs.ParseStarInput import ParseStarInput
from Tests.baseTest import baseTest


class testLandmarksExtremes(baseTest):

    def setUp(self) -> None:
        ParseStarInput.deep_space = {}

    def test_q_extremes_of_zarushagar(self) -> None:
        sourcefile = self.unpack_filename('../DeltaFiles/Zarushagar.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        self.assertIsNotNone(sector, "Sector file not loaded from " + sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        foo = LandmarksQExtremes(galaxy)

        expected = [
                {0: 132, 1: 165, 2: 293, 3: 368, 4: 408, 5: 411, 6: 420, 7: 415},
                {0: 0, 1: 165, 2: 293, 3: 368, 4: 408, 5: 409, 6: 414, 7: 415}
            ]
        actual = foo.get_landmarks(index=True)
        self.assertEqual(expected, actual)

    def test_r_extremes_of_zarushagar(self) -> None:
        sourcefile = self.unpack_filename('../DeltaFiles/Zarushagar.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        self.assertIsNotNone(sector, "Sector file not loaded from " + sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        foo = LandmarksRExtremes(galaxy)

        expected = [
                {0: 0, 1: 165, 2: 293, 3: 368, 4: 408, 5: 411, 6: 414, 7: 415},
                {0: 486, 1: 165, 2: 293, 3: 368, 4: 408, 5: 409, 6: 420, 7: 415}
            ]
        actual = foo.get_landmarks(index=True)
        self.assertEqual(expected, actual)

    def test_s_extremes_of_zarushagar(self) -> None:
        sourcefile = self.unpack_filename('../DeltaFiles/Zarushagar.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        self.assertIsNotNone(sector, "Sector file not loaded from " + sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        foo = LandmarksSExtremes(galaxy)

        expected = [
                {0: 413, 1: 165, 2: 293, 3: 368, 4: 408, 5: 409, 6: 414, 7: 415},
                {0: 126, 1: 165, 2: 293, 3: 368, 4: 408, 5: 411, 6: 416, 7: 415}
            ]
        actual = foo.get_landmarks(index=True)
        self.assertEqual(expected, actual)

    def test_axial_extremes_of_zarushagar(self) -> None:
        sourcefile = self.unpack_filename('../DeltaFiles/Zarushagar.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        self.assertIsNotNone(sector, "Sector file not loaded from " + sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        foo = LandmarksTriaxialExtremes(galaxy)
        self.assertEqual(496, foo.graph_len)
        self.assertIsInstance(foo.distgraph, DistanceGraph)
        self.assertEqual(float('+inf'), foo.floatinf)

        expected = [
            {0: 132, 5: 411, 6: 420},
            {0: 486, 6: 418},
            {0: 126},
            {0: 0},
            {0: 5},
            {0: 428},
        ]
        actual, _ = foo.get_landmarks(index=True)
        self.assertEqual(expected, actual)

        actual, _ = foo.get_landmarks()
        self.assertEqual(6, len(actual))
        chunk = actual[3]
        self.assertEqual(0, chunk[0].index)

    def test_component_landmarks_of_zarushagar(self) -> None:
        sourcefile = self.unpack_filename('../DeltaFiles/Zarushagar.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        self.assertIsNotNone(sector, "Sector file not loaded from " + sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        expected = defaultdict(set)
        expected[0] = {0, 132, 5, 486, 428, 126}
        expected[5] = {411}
        expected[6] = {418, 420}

        foo = LandmarksTriaxialExtremes(galaxy)
        _, actual = foo.get_landmarks(index=True)
        self.assertEqual(expected, actual)

    def test_landmarks_of_dagudashaag(self) -> None:
        sourcefile = self.unpack_filename('../DeltaFiles/Dagudashaag.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        self.assertIsNotNone(sector, "Sector file not loaded from " + sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        expected_components = defaultdict(set)
        expected_components[0] = {129, 6, 138, 555, 427, 558}
        expected_components[2] = {426, 423}

        expected_landmarks = [{0: 555, 2: 426}, {0: 558, 2: 423}, {0: 129}, {0: 138}, {0: 6}, {0: 427}]

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks, actual = foo.get_landmarks(index=True)
        self.assertEqual(expected_components, actual)
        self.assertEqual(expected_landmarks, landmarks)

    def test_max_slots(self) -> None:
        cases = [
            (501, 10),
            (500, 12),
            (499, 12),
            (251, 12),
            (250, 14),
            (249, 14),
            (126, 14),
            (125, 15),
            (124, 15)
        ]

        for route_reuse, expected in cases:
            args = self._make_args()
            delta = DeltaDictionary()

            galaxy = DeltaGalaxy(args.btn, args.max_jump)
            galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                                route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)

            foo = LandmarksTriaxialExtremes(galaxy)
            self.assertEqual(expected, foo.max_slots)
