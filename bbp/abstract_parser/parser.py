from abc import ABC, abstractmethod


class Parser(ABC):
    PARSER_PROGRESS = "PARSER_PROGRESS"

    def __init__(self, *args, source_format_service, context_service, **kwargs):
        self._source_format_service = source_format_service
        self._context_service = context_service

    @abstractmethod
    def __call__(self, tokens, position):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def update_parse_progress(self, tokens, position):
        progress_position = self.__get_progress_position()
        if position > progress_position:
            self._context_service.set_context_variable(
                Parser.PARSER_PROGRESS, {"tokens": tokens, "position": position, "parser_repr": self.__repr__()})

    def __tokens_to_text(self, tokens):
        return self._source_format_service.tokens_to_text(tokens)

    def __get_progress_position(self):
        parser_progress = self.get_parser_progress()
        return parser_progress["position"] if parser_progress else -1

    def get_parser_progress(self):
        return self._context_service.get_context_variable(Parser.PARSER_PROGRESS)

    def clear_parser_progress(self):
        self._context_service.set_context_variable(Parser.PARSER_PROGRESS, None)
