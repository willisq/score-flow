export class Description {
  constructor(value) {
    if (!value || typeof value !== "string" || value.trim().length === 0) {
      throw new Error("La descripción es obligatoria.");
    }

    if (!Description.#VALID_TYPES.has(value)) {
      throw new Error(`El tipo de ronda "${value}" no es un valor válido.`);
    }

    this.value = value;
  }

  static FINAL = "Final";
  static SEMIFINAL = "Semi Final";
  static QUARTERFINAL = "Cuartos de Final";
  static ROUND_OF_16 = "Octavos de Final";
  static ROUND_OF_32 = "Rondas de 32";

  static #VALID_TYPES = new Set([
    Description.FINAL,
    Description.SEMIFINAL,
    Description.QUARTERFINAL,
    Description.ROUND_OF_16,
    Description.ROUND_OF_32,
  ]);
}
