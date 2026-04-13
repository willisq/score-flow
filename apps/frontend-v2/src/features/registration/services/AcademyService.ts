import { httpClient } from "@/core/api/http-client";
import type { Academy, AcademyCreate } from "../types";

export class AcademyService {
  private static readonly BASE = "/registration/academies";

  static async getAll(): Promise<Academy[]> {
    const { data } = await httpClient.get<Academy[]>(this.BASE);
    return data;
  }

  static async create(payload: AcademyCreate): Promise<Academy> {
    const { data } = await httpClient.post<Academy>(this.BASE, payload);
    return data;
  }
}
