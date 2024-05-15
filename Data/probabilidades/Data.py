class Data:
    def retornarDatosTresNodos(self):
        subconjuntos = {
                    "1": {
                        (0, 0, 0): 0, (1, 0, 0): 0, (0, 1, 0): 1, (1, 1, 0): 1,
                        (0, 0, 1): 1, (1, 0, 1): 1, (0, 1, 1): 1, (1, 1, 1): 1

                    },
                    "2": {
                        (0, 0, 0): 0, (1, 0, 0): 0, (0, 1, 0): 0, (1, 1, 0): 0,
                        (0, 0, 1): 0, (1, 0, 1): 1, (0, 1, 1): 0, (1, 1, 1): 1
                    },
                    "3": {
                        (0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 1, (1, 1, 0): 0,
                        (0, 0, 1): 0, (1, 0, 1): 1, (0, 1, 1): 1, (1, 1, 1): 0
                    }
                    }
        return subconjuntos
    
    def retornarDatosCuatroNodos(self):
        subconjuntos = {
                        "1": {
                            (0, 0, 0, 0): 0, (1, 0, 0, 0): 0, (0, 1, 0, 0): 1, (1, 1, 0, 0): 1,
                            (0, 0, 1, 0): 1, (1, 0, 1, 0): 1, (0, 1, 1, 0): 1, (1, 1, 1, 0): 1,
                            (0, 0, 0, 1): 0, (1, 0, 0, 1): 0, (0, 1, 0, 1): 1, (1, 1, 0, 1): 1,
                            (0, 0, 1, 1): 1, (1, 0, 1, 1): 1, (0, 1, 1, 1): 1, (1, 1, 1, 1): 1

                        },
                        "2": {
                            (0, 0, 0, 0): 0, (1, 0, 0, 0): 0, (0, 1, 0, 0): 0, (1, 1, 0, 0): 0,
                            (0, 0, 1, 0): 0, (1, 0, 1, 0): 1, (0, 1, 1, 0): 0, (1, 1, 1, 0): 1,
                            (0, 0, 0, 1): 0, (1, 0, 0, 1): 0, (0, 1, 0, 1): 0, (1, 1, 0, 1): 0,
                            (0, 0, 1, 1): 0, (1, 0, 1, 1): 1, (0, 1, 1, 1): 0, (1, 1, 1, 1): 1
                        },
                        "3": {
                            (0, 0, 0, 0): 0, (1, 0, 0, 0): 1, (0, 1, 0, 0): 1, (1, 1, 0, 0): 0,
                            (0, 0, 1, 0): 0, (1, 0, 1, 0): 1, (0, 1, 1, 0): 1, (1, 1, 1, 0): 0,
                            (0, 0, 0, 1): 0, (1, 0, 0, 1): 1, (0, 1, 0, 1): 1, (1, 1, 0, 1): 0,
                            (0, 0, 1, 1): 0, (1, 0, 1, 1): 1, (0, 1, 1, 1): 1, (1, 1, 1, 1): 0
                        },
                        "4": {
                            (0, 0, 0, 0): 0, (1, 0, 0, 0): 1, (0, 1, 0, 0): 1, (1, 1, 0, 0): 0,
                            (0, 0, 1, 0): 0, (1, 0, 1, 0): 1, (0, 1, 1, 0): 1, (1, 1, 1, 0): 0,
                            (0, 0, 0, 1): 0, (1, 0, 0, 1): 0, (0, 1, 0, 1): 0, (1, 1, 0, 1): 1,
                            (0, 0, 1, 1): 1, (1, 0, 1, 1): 1, (0, 1, 1, 1): 0, (1, 1, 1, 1): 1
                        }

                        }
        return subconjuntos