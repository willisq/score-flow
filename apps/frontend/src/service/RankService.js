import { api } from "@/service/AxiosBaseService";

export class RankService {
  static async findAll() {
    const { data } = await api.get("/rank/");

    return data;
  }
}
