from elt.console_view import _format_table


def test_format_table_renders_headers_and_rows():
    result = _format_table(("name", "value"), (("Montale", 420),))
    assert "name" in result
    assert "Montale" in result
    assert "420" in result


def test_format_table_truncates_long_values():
    result = _format_table(("name",), (("x" * 50,),))
    assert "..." in result
    assert "x" * 50 not in result

