import { httpClient } from "@/core/api/http-client";
import type { Modality, ModalityCreate } from "../types";

export class ModalityService {
  private static readonly BASE = "/tournament/modalities";

  static async getAll(): Promise<Modality[]> {
    const { data } = await httpClient.get<Modality[]>(this.BASE);
    return data;
  }

  static async create(payload: ModalityCreate): Promise<Modality> {
    const { data } = await httpClient.post<Modality>(this.BASE, payload);
    return data;
  }
}
