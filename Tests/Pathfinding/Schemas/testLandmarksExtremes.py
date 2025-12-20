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
from PyRoute.Pathfinding.LandmarkSchemes.LandmarksWTNExtremes import LandmarksWTNExtremes
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
            {0: 486, 5: 409, 6: 418},
            {0: 126},
            {0: 0},
            {0: 5},
            {0: 428},
            {0: 140}
        ]
        actual, _ = foo.get_landmarks()
        self.assertEqual(expected, actual)

        actual, _ = foo.get_landmarks()
        self.assertEqual(7, len(actual))
        chunk = actual[3]
        self.assertEqual(0, chunk[0])

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
        expected[0] = {0, 132, 5, 486, 428, 140, 126}
        expected[5] = {409, 411}
        expected[6] = {418, 420}

        foo = LandmarksTriaxialExtremes(galaxy)
        _, actual = foo.get_landmarks()
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

        btn = [(s, n, d) for (s, n, d) in galaxy.ranges.edges(data=True) if s.component == n.component]
        btn.sort(key=lambda tn: tn[2]['btn'], reverse=True)

        expected_components = defaultdict(set)
        expected_components[0] = {129, 165, 6, 138, 555, 427, 558}
        expected_components[2] = {426, 423}

        expected_landmarks = [{0: 555, 2: 426}, {0: 558, 2: 423}, {0: 129}, {0: 138}, {0: 6}, {0: 427}, {0: 165}]

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks, actual = foo.get_landmarks(btn=btn)
        self.assertEqual(expected_components, actual)
        self.assertEqual(expected_landmarks, landmarks)

    def test_landmarks_of_dagudashaag_and_zarushagar(self) -> None:
        source1 = self.unpack_filename('../DeltaFiles/Dagudashaag.sec')
        source2 = self.unpack_filename('../DeltaFiles/Zarushagar.sec')

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(source1)
        self.assertIsNotNone(sector, "Sector file not loaded from " + source1)
        delta[sector.name] = sector
        sector = SectorDictionary.load_traveller_map_file(source2)
        self.assertIsNotNone(sector, "Sector file not loaded from " + source1)
        delta[sector.name] = sector

        args = self._make_args()
        args.max_jump = 3

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        expected_components = defaultdict(set)
        expected_components[0] = {129, 6, 967, 138, 555, 1045, 1051, 989}
        expected_components[5] = {968, 970}
        expected_components[6] = {977, 979, 974}
        expected_landmarks = [{0: 555, 5: 970, 6: 979}, {0: 1045, 5: 968, 6: 977}, {0: 129, 6: 974}, {0: 138}, {0: 6},
                              {0: 967}, {0: 989}, {0: 1051}]

        foo = LandmarksTriaxialExtremes(galaxy)
        landmarks, actual = foo.get_landmarks()
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

    def test_landmarks_on_ibara_subsector_single_component(self) -> None:
        sourcefile = self.unpack_filename('DeltaFiles/Zarushagar-Ibara.sec')

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

        self.assertEqual(1, len(galaxy.trade.components), "Unexpected number of components at J-4")

        expected_landmarks = [{0: 34}, {0: 30}, {0: 27}, {0: 0}]
        landmarks, _ = galaxy.trade.get_landmarks()
        self.assertTrue(isinstance(landmarks, list), 'Landmarks result should be a list')
        self.assertEqual(expected_landmarks, landmarks, 'Unexpected landmark result')

    def test_landmarks_on_ibara_subsector_multiple_components(self) -> None:
        sourcefile = self.unpack_filename('DeltaFiles/Zarushagar-Ibara.sec')

        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta = DeltaDictionary()
        delta[sector.name] = sector

        args = self._make_args()
        args.max_jump = 1

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()
        galaxy.trade.calculate_components()

        self.assertEqual(6, len(galaxy.trade.components), "Unexpected number of components at J-1")

        expected_landmarks = [{0: 29, 2: 13, 4: 34}, {0: 26, 2: 4, 4: 36}, {0: 19, 4: 27}, {0: 0}]
        landmarks, _ = galaxy.trade.get_landmarks()
        self.assertEqual(4, len(landmarks), 'Should have one landmark per component')
        self.assertEqual(expected_landmarks, landmarks, 'Unexpected landmark result')

    def test_wtn_landmarks_on_ibara_subsector_single_component(self) -> None:
        sourcefile = self.unpack_filename('DeltaFiles/Zarushagar-Ibara.sec')

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

        foo = LandmarksWTNExtremes(galaxy)
        exp_landmarks = [{0: 18}]
        landmarks = foo.get_landmarks()
        self.assertEqual(exp_landmarks, landmarks)
