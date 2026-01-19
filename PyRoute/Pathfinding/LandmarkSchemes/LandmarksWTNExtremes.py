"""
Created on Feb 19, 2024

@author: CyberiaResurrection
"""


class LandmarksWTNExtremes:

    def __init__(self, galaxy):
        self.galaxy = galaxy

    def get_landmarks(self) -> list[dict]:
        result = []

        result.append(dict())
        for component_id in self.galaxy.trade.components:
            stars = [item for item in self.galaxy.star_mapping.values() if component_id == item.component]
            source = max(stars, key=lambda item: item.wtn)
            result[0][component_id] = source.index

        return result
