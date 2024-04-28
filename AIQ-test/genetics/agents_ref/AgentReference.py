class AgentReference:
    """
    Base class that is used as reference for real Agent in AIQ test.

    This class contains generator methods for agents parameters as well the link
    to original AIQ agent.
    """
    def generate_params(self):
        """
        Creates list of parameters by its generator functions.
        """
        generator = self.get_generators()
        params = list()
        for g in generator:
            params.append(g())
        return params

    def get_test_agent_name(self):
        """
        Returns name of the AIQ agent's class in ./agents folder.
        """
        raise NotImplemented()

    def get_generators(self):
        """
        Returns sequential list of functions that generates parameters for AIQ agent.
        """
        raise NotImplemented()
        return list()
