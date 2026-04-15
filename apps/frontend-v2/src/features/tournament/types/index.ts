import type { Competitor, Rank, Sex } from "@/features/registration/types";

// --- Base Entities ---

export interface Modality {
  id: string;
  name: string;
}

export interface Tournament {
  id: string;
  description: string;
}

export interface Category {
  id: string;
  ages: number[];
  specialCondition: boolean;
  modality: Modality;
  ranks: Rank[];
  sexes: Sex[];
  initialWeight: number | null;
  finalWeight: number | null;
  initialHeight: number | null;
  finalHeight: number | null;
}

export interface CategoryRegistration {
  id: string;
  competitor: Competitor;
  category: Category;
  tournament: Tournament;
}

// --- Create DTOs ---

export interface ModalityCreate {
  name: string;
}

export interface TournamentCreate {
  description: string;
}

export interface CategoryCreate {
  ages: number[];
  specialCondition?: boolean;
  modalityIds: string[];
  rankIds: string[];
  sexIds: string[];
  initialWeight?: number | null;
  finalWeight?: number | null;
  initialHeight?: number | null;
  finalHeight?: number | null;
}

export interface CategoryRegistrationCreate {
  competitorId: string;
  categoryId: string;
  tournamentId: string;
}

// --- Mass Registration ---

export interface MassRegistrationRequest {
  competitorIds: string[];
  tournamentId: string;
  categoryId?: string | null;
}

export interface RegistrationError {
  competitorId: string;
  competitorName: string;
  message: string;
  reasons?: Record<string, boolean>;
  overlappingCategories?: Category[];
}

export interface MassRegistrationResponse {
  registrations: CategoryRegistration[];
  errors: RegistrationError[];
}
