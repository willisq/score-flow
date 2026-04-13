import { httpClient } from "@/core/api/http-client";
import type {
  CategoryRegistration,
  CategoryRegistrationCreate,
  MassRegistrationRequest,
  MassRegistrationResponse,
} from "../types";

export class InscriptionService {
  private static readonly BASE = "/tournament";

  static async inscribe(payload: CategoryRegistrationCreate): Promise<CategoryRegistration> {
    const { data } = await httpClient.post<CategoryRegistration>(
      `${this.BASE}/inscriptions`,
      payload,
    );
    return data;
  }

  static async massRegister(payload: MassRegistrationRequest): Promise<MassRegistrationResponse> {
    const { data } = await httpClient.post<MassRegistrationResponse>(
      `${this.BASE}/mass-registration`,
      payload,
    );
    return data;
  }
}
