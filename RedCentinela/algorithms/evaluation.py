import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """ 
    # TODO: Add your code here
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    value = float(state.get_score())
    defender = state.defender_position
    intruder = state.intruder_position
    terminals = state.pending_terminals
    value -= 30.0 * len(terminals)

    if terminals:
        distances = [
            state.layout.distance(defender, terminal)
            for terminal in terminals
        ]

        finite_distances = [
            distance
            for distance in distances
            if math.isfinite(distance)
        ]

        if finite_distances:
            value -= 5.0 * min(finite_distances)

    intruder_distance = state.layout.distance(defender, intruder)

    if math.isfinite(intruder_distance):
        if intruder_distance <= 1:
            value -= 200.0
        elif intruder_distance == 2:
            value -= 80.0
        else:
            value += min(intruder_distance, 10) * 3.0

    value += 2.0 * len(state.get_legal_actions(0))

    return max(-999.0, min(999.0, value))