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

export interface PhysicalRequirement {
  id: string;
  initialWeight: number | null;
  finalWeight: number | null;
  initialHeight: number | null;
  finalHeight: number | null;
}

export interface CategoryModality {
  id: string;
  modality: Modality;
  physicalRequirement: PhysicalRequirement | null;
}

export interface Category {
  id: string;
  ages: number[];
  specialCondition: boolean;
  ranks: Rank[];
  sexes: Sex[];
  modalities: CategoryModality[];
}

export interface CategoryRegistration {
  id: string;
  competitor: Competitor;
  categoryModality: CategoryModality;
  tournament: Tournament;
}

// --- Create DTOs ---

export interface ModalityCreate {
  name: string;
}

export interface TournamentCreate {
  description: string;
}

export interface PhysicalRequirementCreate {
  initialWeight?: number | null;
  finalWeight?: number | null;
  initialHeight?: number | null;
  finalHeight?: number | null;
}

export interface CategoryModalityCreate {
  modalityId: string;
  physicalRequirement?: PhysicalRequirementCreate | null;
}

export interface CategoryCreate {
  ages: number[];
  specialCondition?: boolean;
  rankIds: string[];
  sexIds: string[];
  modalities: CategoryModalityCreate[];
}

export interface CategoryUpdate {
  ages?: number[];
  specialCondition?: boolean;
  rankIds?: string[];
  sexIds?: string[];
  modalities?: CategoryModalityCreate[];
}

export interface CategoryRegistrationCreate {
  competitorId: string;
  categoryModalityId: string;
  tournamentId: string;
}

// --- Mass Registration ---

export interface MassRegistrationRequest {
  competitorIds: string[];
  tournamentId: string;
  categoryModalityId?: string | null;
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

export interface CategoryBulkCreate {
  categories: CategoryCreate[];
}
