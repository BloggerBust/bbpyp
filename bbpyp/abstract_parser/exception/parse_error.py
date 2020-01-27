from bbpyp.common.exception.bbpyp_exception import BbpypException


class ParseError(BbpypException):
    def __init__(self, tokens, position, *args, source_format_service, **kwargs):
        end_position = source_format_service.get_index_of_next_line_separator_position(
            tokens, position) + 1
        what = source_format_service.tokens_to_text(tokens[:end_position])
        super().__init__(what, *args, **kwargs)

        self._position = position
        self._src_path = None

        column_of_position = source_format_service.get_column_of_position(tokens, position)
        self._position_indicator = f"{'':-^{column_of_position}}^"

    def __repr__(self):
        representation = f"{self.who}: {self.why}\nParsing stopped at position {self._position}\n{self.src}\n{self._position_indicator}"

        if self.src_path:
            representation = f"{representation}\nsrc: {self.src_path}"

        if self.inner_exception:
            representation += f"\nCaused By:{self.inner_exception}"

        return representation

    @property
    def src(self):
        return self._what

    @property
    def src_path(self):
        return self._src_path

    @src_path.setter
    def src_path(self, value):
        self._src_path = value
