from ..src.format import format_title_to_apa
import pytest

def test_format_to_api():

    test_1 = 'A Century of Work Teams in the Journal of Applied Psychology'
    out_1 = 'A Century of Work Teams in the Journal of Applied Psychology'
    assert out_1 == format_title_to_apa(test_1)

    test_2 = 'WHEN AND HOW TEAM LEADERS MATTER'
    out_2 = 'When and How Team Leaders Matter'
    assert out_2 == format_title_to_apa(test_2)

    test_3 = 'Perspective: Teams Won\'t Solve This Problem'
    out_3 = "Perspective: Teams Won’t Solve This Problem"
    assert out_3 == format_title_to_apa(test_3)

    test_4 = 'Learning more by crossing levels: evidence from airplanes, hospitals, and orchestras'
    out_4 = 'Learning More by Crossing Levels: Evidence From Airplanes, Hospitals, and Orchestras'
    assert out_4 == format_title_to_apa(test_4)
