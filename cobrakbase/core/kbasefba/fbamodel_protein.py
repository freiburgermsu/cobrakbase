from cobra.core import Group


class ModelReactionProteinSubunit:
    """
        typedef structure {
      string role;
      bool triggering;
      bool optionalSubunit;
      string note;
      list<feature_ref> feature_refs;
    } ModelReactionProteinSubunit;
    """

    def __init__(
        self, role: None, triggering: None, optional: None, note: None, features: list
    ):
        """

        @param role:  'role': 'ftr06142'
        @param triggering: 'triggering': 1
        @param optional: 'optionalSubunit': 0,
        @param note:
        @param features: ['~/genome/features/id/b2930', '~/genome/features/id/b3925']
        """
        self.role = role
        if triggering is not None:
            self.triggering = bool(triggering)
        else:
            self.triggering = None
        if optional is not None:
            self.optional = bool(optional)
        else:
            self.optional = None
        self.note = note
        self.features = features

    @staticmethod
    def from_json(data):
        return ModelReactionProteinSubunit(
            data.get("role", None),
            data.get("triggering", None),
            data.get("optionalSubunit", None),
            data.get("note", None),
            data["feature_refs"],
        )

    def get_data(self):
        d = {"feature_refs": self.features}
        if self.role is not None:
            d["role"] = self.role
        if self.note is not None:
            d["note"] = self.note
        if self.optionalSubunit is not None:
            d["optionalSubunit"] = 0
            if self.optionalSubunit:
                d["optionalSubunit"] = 1
        if self.triggering is not None:
            d["triggering"] = 0
            if self.triggering:
                d["triggering"] = 1
                
        return d


class ModelReactionProtein(Group):
    """
        @optional source complex_ref
    */
    typedef structure {
      complex_ref complex_ref;
      string note;
      list<ModelReactionProteinSubunit> modelReactionProteinSubunits;
      string source;
    } ModelReactionProtein;
    """

    def __init__(self, complex_id, note: str, source: str, subunits: list, cpx=None):
        """

        @param note:
        @param source:
        @param subunits: list of ModelReactionProteinSubunit
        @param cpx:  ~/template/complexes/name/cpx01517
        """
        super().__init__(complex_id)
        self.subunits = subunits
        self.note = note
        self.source = source
        self.cpx = cpx

    @staticmethod
    def from_json(data):
        subunits = [
            ModelReactionProteinSubunit.from_json(o)
            for o in data["modelReactionProteinSubunits"]
        ]

        complex_id = data.get("complex_ref")
        return ModelReactionProtein(
            complex_id, data.get("note"), data.get("source"), subunits, complex_id
        )

    def get_data(self):
        d = {"modelReactionProteinSubunits": [x.get_data() for x in self.subunits]}
        if self.note:
            d["note"] = self.note
        if self.source:
            d["source"] = self.source
        if self.cpx:
            d["complex_ref"] = self.cpx
        return d

    def __repr__(self):
        ands = []
        for o in self.subunits:
            ors = {o.split("/")[-1] for o in o.features}
            rule = " or ".join(ors)
            if len(ors) > 1:
                ands.append(f"({rule})")
            else:
                ands.append(rule)
        return " and ".join(ands)

    def __str__(self):
        return self.__repr__()
