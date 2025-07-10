import { api } from "@/service/AxiosBaseService";

export class SexService {
  static async findAll() {
    const { data } = await api.get("/sex/");

    return data;
  }
}
