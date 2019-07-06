from copy import deepcopy
from bbp.tag_script.parser.statement import Statement
from bbp.tag_script.parser.real_number import RealNumber
from bbp.tag_script.parser.access import Access
from bbp.tag_script.parser.model.result import Result
from bbp.abstract_parser.exception.parse_error import ParseError


class TagStatement(Statement):
    PARSED_CACHE = {}

    def __init__(self, tag, rest, parser_service, lexer_service, scripts_path, file_stream_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser = parser_service
        self._lexer = lexer_service
        self._tag = tag
        self._rest = rest
        self._scripts_path = scripts_path
        self._file_stream_service = file_stream_service
        self._tag_file = f"{scripts_path}{self._tag.name}.ts"

    def __repr__(self):
        return f"{self.artifact_name}({self._tag, self._rest})"

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return self._tag == other._tag and self._rest == other._rest and self._tag_file == other._tag_file

    def __hash__(self):
        return hash(tuple(self._tag, self._rest))

    def _eval(self, frame):
        return_value = None
        new_frame = {}
        argument_names = self._push_arguments_on_frame(new_frame)
        new_frame = self._push_hash_table_from_results_frame_onto_new_frame(frame, new_frame)
        self._set_is_unwinding(frame, False)
        self._push_frame_onto_call_stack(frame, new_frame)
        parser = self._get_parser()
        return_value = None

        if parser is not None:
            return_value = parser.eval(new_frame)
            if return_value is not None:
                results_frame = self._get_results_frame(frame)
                self._tag(results_frame, return_value)
                return_value = self._tag.eval(results_frame)

        self._pop_arguments_from_frame(new_frame, argument_names)
        self._update_hash_table_of_results_frame_with_hash_table_from_new_frame(frame, new_frame)
        popped_frame = self._pop_frame_from_call_stack(frame)
        assert popped_frame == new_frame

        return return_value

    @classmethod
    def _push_frame_onto_call_stack(cls, frame, new_frame):
        if cls.CALL_STACK_KEY not in frame:
            frame[cls.CALL_STACK_KEY] = []

        stack = cls._get_call_stack(frame)
        cls._set_call_stack(new_frame, stack)
        stack.append(new_frame)

    @classmethod
    def _push_hash_table_from_results_frame_onto_new_frame(cls, frame, new_frame):
        results_frame = cls._get_results_frame(frame)
        resulting_frame = {**new_frame, **results_frame}
        return resulting_frame

    @classmethod
    def _update_hash_table_of_results_frame_with_hash_table_from_new_frame(cls, frame, new_frame):
        old_results = cls._get_results_frame(frame)
        updated_results = {**old_results}
        new_result = cls._get_results_frame(new_frame)
        for new_result_item in new_result.items():
            key, new_result_value = new_result_item
            if key in updated_results and type(updated_results[key]) is dict and type(new_result_value) is dict:
                new_result[key] = {**updated_results[key], **new_result_value}

        merged_results = {**updated_results, **new_result}
        #assert old_results == merged_results

        cls._set_results_frame(frame, merged_results)

    @classmethod
    def _pop_frame_from_call_stack(cls, frame):
        return frame[cls.CALL_STACK_KEY].pop()

    def _push_arguments_on_frame(self, frame):
        argument_names = []
        argument_values = []
        index = 0
        for tag in self._rest:
            argument_name = f"arg{index}"
            if type(tag) is Access:
                frame[f"arg{index}"] = f"{tag.name}"

            elif type(tag) is RealNumber:
                frame[f"arg{index}"] = tag.value
            else:
                raise Exception(f"unsupported argument tag type = {type(tag)}")

            argument_values.append(frame[argument_name])
            index += 1
            argument_names.append(argument_name)

        frame["args"] = argument_values

        return argument_names

    @classmethod
    def _pop_arguments_from_frame(cls, frame, argument_names):
        index = 0
        for argument_name in argument_names:
            del frame[argument_name]
            index += 1
        del frame["args"]

    def _get_tokens(self):
        if not self._file_stream_service.is_file(self._tag_file):
            raise NotImplementedError(f"Tag implementaton not found for {self._tag_file}")

        script = self._file_stream_service.read_text_from_file(self._tag_file)
        return self._lexer.tokenize(script)

    def _get_parser(self):

        if self._tag_file in TagStatement.PARSED_CACHE:
            cached_result = TagStatement.PARSED_CACHE[self._tag_file]
            return deepcopy(cached_result)

        try:
            tokens = self._get_tokens()
            result = self._parser(tokens, 0)
            TagStatement.PARSED_CACHE[self._tag_file] = deepcopy(result.value)
            return result.value
        except (ParseError, TypeError) as e:
            e.src_path = self._tag_file
            raise e
