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

  static async delete(categoryModalityId: string): Promise<void> {
    await httpClient.delete(`${this.BASE}/${categoryModalityId}`);
  }

  static async removeCompetitor(categoryModalityId: string, registrationId: string, removeFromCategory: boolean = false): Promise<GenerateBracketsResponse> {
    const { data } = await httpClient.delete<GenerateBracketsResponse>(
      `${this.BASE}/${categoryModalityId}/competitor/${registrationId}`,
      { params: { remove_registration: removeFromCategory } }
    );
    return data;
  }

  static async moveCompetitor(
    sourceCmId: string,
    registrationId: string,
    payload: {
      targetCategoryModalityId: string;
      competitorId: string;
      newWeight?: number;
      newAge?: number;
      newRankId?: string;
    }
  ): Promise<GenerateBracketsResponse> {
    const { data } = await httpClient.post<GenerateBracketsResponse>(
      `${this.BASE}/${sourceCmId}/competitor/${registrationId}/move`,
      payload
    );
    return data;
  }
}
