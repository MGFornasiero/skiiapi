// models.ts

// =============================================================
// Custom Enum Types from DDL
// =============================================================

export type GradeType = 'kyu' | 'dan';

export type Sides = 'sx' | 'frontal' | 'dx';

export type Movements = 'Fwd' | 'Still' | 'Bkw';

export type KataSeries = 'Heian' | 'Tekki' | 'Sentei';

export type TargetHgt = 'Jodan' | 'Chudan' | 'Gedan';

export type WazaType = 'Uke' | 'Uchi' | 'Geri' | 'NA' | '_';

export type Tempo = 'Legato' | 'Fast' | 'Normal' | 'Slow' | 'Breath';

export type Limbs = 'Mano' | 'Braccio' | 'Piede' | 'Gamba' | 'Ginochio' | 'NA';

export type Hips = 'Hanmi' | 'Shomen';

export type BeltColor = 'bianco' | 'giallo' | 'arancio' | 'verde' | 'blu' | 'marrone' | 'nero';

export type AbsoluteDirections = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SO' | 'O' | 'NO';

// =============================================================
// Custom Composite Types from DDL
// =============================================================

export interface EmbusenPoints {
    x: number;
    y: number;
}

export interface BodyPart {
    limb: Limbs;
    side: Sides;
}

export interface DetailedNotes {
    arto: BodyPart;
    description?: string;
    explatation?: string;
    note?: string;
}

// =============================================================
// Domain Table Models (ski schema) and functions (public schema)
// =============================================================

export interface Target {
    id_target: number;
    name: string;
    original_name?: string;
    description?: string;
    notes?: string;
    resource_url?: string;
}

export interface StrikingPart {
    id_part: number;
    name: string;
    translation?: string;
    description?: string;
    notes?: string;
    resource_url?: string;
}

export interface Technic {
    id_technic: number;
    waza?: WazaType;
    name: string;
    description?: string;
    notes?: string;
    resource_url?: string;
}

export interface TechnicDecomposition {
    id_decomposition: number;
    technic_id: number;
    component_order: number;
    description?: string;
    explatations?: string;
    notes?: string;
    resource_url?: string;
}

export interface Stand {
    id_stand: number;
    name: string;
    description?: string;
    illustration_url?: string;
    notes?: string;
}

export interface Grade {
    id_grade: number;
    gtype: GradeType;
    grade: number;
    color?: BeltColor;
}

export interface KihonInventory {
    id_inventory: number;
    grade_id: number;
    number: number;
    resources?: Record<string, any>;
    notes?: string;
}

export interface KihonSequence {
    id_sequence: number;
    inventory_id: number;
    seq_num: number;
    stand_id: number;
    technic_id: number;
    hips?: Hips;
    gyaku?: boolean;
    target_hgt?: TargetHgt;
    resources?: Record<string, any>;
    notes?: string;
    resource_url?: string;
}

export interface KihonTx {
    id_tx: number;
    from_sequence: number;
    to_sequence: number;
    movement?: Movements;
    resources?: Record<string, any>;
    notes?: string;
    tempo?: Tempo;
    resource_url?: string;
}

export interface KihonStep {
    id_sequence: number;
    inventory_id: number;
    seq_num: number;
    stand_id: number;
    technic_id: number;
    gyaku: boolean | null;
    target_hgt: TargetHgt | null;
    notes: string | null;
    resource_url: string | null;
    stand_name: string | null;
    technic_name: string | null;
}

export interface KihonFormatted {
    number: number;
    seq_num: number;
    movement: Movements | null;
    technic_id: number;
    gyaku: boolean | null;
    tecnica: string | null;
    stand_id: number;
    posizione: string | null;
    target_hgt: TargetHgt | null;
    notes: string | null;
}

export interface KataInventory {
    id_kata: number;
    kata: string;
    serie?: KataSeries;
    starting_leg: Sides;
    notes?: string;
    resources?: Record<string, any>;
    resource_url?: string;
}

export interface KataSequence {
    id_sequence: number;
    kata_id: number;
    seq_num: number;
    stand_id: number;
    speed?: Tempo;
    side?: Sides;
    hips?: Hips;
    embusen?: EmbusenPoints;
    facing?: AbsoluteDirections;
    kiai?: boolean;
    notes?: string;
    remarks?: DetailedNotes[];
    resources?: Record<string, any>;
    resource_url?: string;
}

export interface KataSequenceWaza {
    id_kswaza: number;
    sequence_id?: number;
    arto?: BodyPart;
    technic_id: number;
    strikingpart_id?: number;
    technic_target_id?: number;
    notes?: string;
    resources?: Record<string, any>;
}

export interface KataTx {
    id_tx: number;
    from_sequence: number;
    to_sequence: number;
    tempo?: Tempo;
    direction?: Sides;
    intermediate_stand_id?: number;
    notes?: string;
    remarks?: DetailedNotes[];
    resources?: Record<string, any>;
    resource_url?: string;
}

export interface KataTechnique {
    sequence_id: number;
    arto: BodyPart;
    technic_id: number;
    tecnica?: string | null;
    technic_target_id?: number | null;
    obiettivo?: string | null;
    waza_note?: string | null;
    waza_resources?: Record<string, any> | null;
}

export interface KataSequenceStep {
    id_sequence: number;
    kata_id: number;
    seq_num: number;
    stand_id: number;
    posizione: string | null;
    guardia: Sides | null;
    facing: AbsoluteDirections | null;
    tecniche: KataTechnique[];
    embusen: EmbusenPoints | null;
    kiai: boolean | null;
    notes: string | null;
    remarks: DetailedNotes[] | null;
    resources: Record<string, any> | null;
    resource_url: string | null;
}

export interface BunkaiInventory {
    id_bunkai: number;
    kata_id: number;
    version?: number;
    name: string;
    description?: string;
    notes?: string;
    resources?: Record<string, any>;
    resource_url?: string;
}

export interface BunkaiSequence {
    id_bunkaisequence: number;
    bunkai_id: number;
    kata_sequence_id: number;
    description?: string;
    notes?: string;
    remarks?: DetailedNotes[];
    resources?: Record<string, any>;
    resource_url?: string;
}


// =============================================================
// API Response Models
// =============================================================

export interface TargetResponse {
    message: string;
    target: Target[];
}