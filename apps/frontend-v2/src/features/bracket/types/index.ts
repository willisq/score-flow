import type { Competitor } from "@/features/registration/types";

// --- Base Entities ---

export interface Round {
  id: string;
  description: string;
}

export interface Match {
  id: string;
  round: Round;
  position: number;
  categoryModalityId: string | null;
  firstCompetitor: Competitor;
  secondCompetitor: Competitor | null;
  winner: Competitor | null;
}

// --- Request / Response DTOs ---

export interface GenerateBracketsRequest {
  categoryModalityIds?: string[] | null;
}

export interface GeneratedCategoryResult {
  categoryModalityId: string;
  matchesGenerated: number;
}

export interface GenerateBracketsResponse {
  results: GeneratedCategoryResult[];
}
