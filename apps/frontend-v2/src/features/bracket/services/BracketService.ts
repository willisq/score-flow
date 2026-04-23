import { httpClient } from "@/core/api/http-client";
import type {
  GenerateBracketsRequest,
  GenerateBracketsResponse,
  Match,
} from "../types";

export class BracketService {
  private static readonly BASE = "/pyramid";

  static async getAll(filters: any = {}): Promise<Match[]> {
    const { data } = await httpClient.get<Match[]>(this.BASE, {
      params: filters,
    });
    return data;
  }

  static async generate(payload: GenerateBracketsRequest): Promise<GenerateBracketsResponse> {
    const { data } = await httpClient.post<GenerateBracketsResponse>(
      `${this.BASE}/generate`,
      payload,
    );
    return data;
  }
}
