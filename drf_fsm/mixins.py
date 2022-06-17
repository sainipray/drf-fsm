from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView


class FsmViewSetMixin(APIView):
    fsm_fields = []

    @classmethod
    def get_fsm_fields(cls):
        return cls.fsm_fields

    @classmethod
    def get_all_transitions(cls, field_name):
        model = cls.queryset.model
        field = getattr(model, field_name).field
        transitions = field.get_all_transitions(model)
        filter_transitions = cls.filter_transitions(field_name, transitions)
        return filter_transitions

    @classmethod
    def filter_transitions(cls, field_name, transitions):
        """
            @classmethod
            def status_transitions(cls):
                return ['pending', 'complete']

        """
        transitions_state_method_name = f"{field_name}_transitions"
        transitions_state_method = getattr(cls, transitions_state_method_name, None)
        if transitions_state_method and callable(transitions_state_method):
            transitions_name = transitions_state_method()
            transitions = filter(lambda x: x.name in transitions_name, transitions)
        return transitions

    @classmethod
    def get_extra_actions(cls):
        """
        Get the methods that are marked as an extra ViewSet `@action`.

        """
        actions = super().get_extra_actions()
        for field in cls.get_fsm_fields():
            transition = cls.get_all_transitions(field)
            for state in transition:
                @action(methods=['post'], detail=True,
                        url_path=f"{field}/{state.name}",
                        url_name=f"{field}-{state.name}-transition", name=f"{field} {state.name}".title(),
                        serializer_class=cls.get_fsm_serializer_class(field, state.name))
                def inner_func(self, request, *args, **kwargs):
                    instance = self.get_object()
                    serializer_class = cls.get_fsm_serializer_class(field, self.action)
                    serializer = serializer_class(data=request.data, instance=instance,
                                                  context={"request": request, "field": field, "action": self.action})
                    serializer.is_valid(raise_exception=True)

                    # Calling transition method
                    getattr(instance, self.action)()
                    instance.save()
                    data = self.get_fsm_serializer_data(serializer, self.action)
                    return Response(data)

                inner_func.__name__ = state.name
                inner_func.mapping = {'post': state.name}
                setattr(cls, state.name, inner_func)
                actions.append(inner_func)

        return actions

    @classmethod
    def get_fsm_serializer_class(cls, field, action_name):
        """
        ex: field = status
            action_name = live
        first trying to find {field}_{action_name}_serializer_class
            serializer_class = status_live_serializer_class

        if above class not exist then finding {field}_serializer_class
            serializer_class = status_serializer_class

         still not exist above then using default serializer_class of view
        """
        field_action_serializer_class_name = f"{action_name}_{field}_serializer_class"
        field_action_serializer_class = getattr(cls, field_action_serializer_class_name, None)
        if field_action_serializer_class:
            return field_action_serializer_class
        return getattr(cls, f"{field}_serializer_class", cls.serializer_class)

    def get_fsm_serializer_data(self, serializer, action_name):
        response_method_name = f"{action_name}_response"
        response_method = getattr(self, response_method_name, None)
        if response_method and callable(response_method):
            return response_method(serializer)
        return serializer.data
