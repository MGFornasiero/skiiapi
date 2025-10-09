from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


def format_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, str):
        # Escape single quotes in string values for SQL safety
        return f"$${v}$$"
    return str(v)

# =============================================================
# Custom Enum Types from DDL
# =============================================================

class GradeType(str, Enum):
    kyu = 'kyu'
    dan = 'dan'

class Sides(str, Enum):
    sx = 'sx'
    frontal = 'frontal'
    dx = 'dx'

class Movements(str, Enum):
    Fwd = 'Fwd'
    Still = 'Still'
    Bkw = 'Bkw'

class KataSeries(str, Enum):
    Heian = 'Heian'
    Tekki = 'Tekki'
    Sentei = 'Sentei'

class TargetHgt(str, Enum):
    Jodan = 'Jodan'
    Chudan = 'Chudan'
    Gedan = 'Gedan'

class WazaType(str, Enum):
    Uke = 'Uke'
    Uchi = 'Uchi'
    Geri = 'Geri'
    NA = 'NA'
    _ = '_'

class Tempo(str, Enum):
    Legato = 'Legato'
    Fast = 'Fast'
    Normal = 'Normal'
    Slow = 'Slow'
    Breath = 'Breath'

class Limbs(str, Enum):
    Mano = 'Mano'
    Braccio = 'Braccio'
    Piede = 'Piede'
    Gamba = 'Gamba'
    Ginochio = 'Ginochio'
    NA = 'NA'

class Hips(str, Enum):
    Hanmi = 'Hanmi'
    Shomen = 'Shomen'

class BeltColor(str, Enum):
    bianco = 'bianco'
    giallo = 'giallo'
    arancio = 'arancio'
    verde = 'verde'
    blu = 'blu'
    marrone = 'marrone'
    nero = 'nero'

class AbsoluteDirections(str, Enum):
    N = 'N'
    NE = 'NE'
    E = 'E'
    SE = 'SE'
    S = 'S'
    SO = 'SO'
    O = 'O'
    NO = 'NO'

# =============================================================
# Custom Composite Types from DDL
# =============================================================

class EmbusenPoints(BaseModel):
    x: int
    y: int

class BodyPart(BaseModel):
    limb: Limbs
    side: Sides

class DetailedNotes(BaseModel):
    arto: BodyPart
    description: Optional[str] = None
    explatation: Optional[str] = None
    note: Optional[str] = None

# =============================================================
# Domain Table Models (ski schema) and functions (public schema)
# =============================================================


class Target(BaseModel): # ski.targets , public.get_targets(), public.get_target_info(), public.qry_ts_targets()
    id_target: int
    name: str
    original_name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None
    
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in Target.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'Target':
        return Target(
            id_target=row[0],
            name=row[1],
            original_name=row[2],
            description=row[3],
            notes=row[4],
            resource_url=row[5]
        )



class StrikingPart(BaseModel): # ski.strikingparts() , public.get_strikingparts(), public.get_strikingparts_info(), public.qry_ts_strikingparts()
    id_part: int
    name: str
    translation: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in StrikingPart.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'StrikingPart':
        return StrikingPart(
            id_part=row[0],
            name=row[1],
            translation=row[2],
            description=row[3],
            notes=row[4],
            resource_url=row[5]
        )


class Technic(BaseModel): # ski.technics() , public.get_technics(), public.get_technic_info(), public.qry_ts_technics()
    id_technic: int
    waza: Optional[WazaType] = None
    name: str
    description: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in Technic.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'Technic':
        return Technic(
            id_technic=row[0],
            waza=row[1],
            name=row[2],
            description=row[3],
            notes=row[4],
            resource_url=row[5]
        )  

class TechnicDecomposition(BaseModel):
    id_decomposition: int
    technic_id: int
    component_order: int
    description: Optional[str] = None
    explatations: Optional[str] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in TechnicDecomposition.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'TechnicDecomposition':
        return TechnicDecomposition(
            id_decomposition=row[0],
            technic_id=row[1],
            component_order=row[2],
            description=row[3],
            explatations=row[4],
            notes=row[5],
            resource_url=row[6]
        )


class Stand(BaseModel):# ski.stands() , public.get_stands(), public.get_stand_info(), public.qry_ts_stands()
    id_stand: int
    name: str
    description: Optional[str] = None
    illustration_url: Optional[str] = None
    notes: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in Stand.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'Stand':
        return Stand(
            id_stand=row[0],
            name=row[1],
            description=row[2],
            illustration_url=row[3],
            notes=row[4]
        )  

class Grade(BaseModel): # ski.grades() , public.get_grade()
    id_grade: int
    gtype: GradeType
    grade: int = Field(..., ge=1, le=10)
    color: Optional[BeltColor] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in Grade.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'Grade':
        return Grade(
            id_grade=row[0],
            gtype=row[1],
            grade=row[2],
            color=row[3]
        )


class KihonInventory(BaseModel): # ski.kihon_inventory() , public.get_kihons()
    id_inventory: int
    grade_id: int
    number: int
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KihonInventory.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KihonInventory':
        return KihonInventory(
            id_inventory=row[0],
            grade_id=row[1],
            number=row[2],
            resources=row[3],
            notes=row[4]
        )

class KihonSequence(BaseModel):
    id_sequence: int
    inventory_id: int
    seq_num: int
    stand_id: int
    technic_id: int
    hips: Optional[Hips] = None
    gyaku: Optional[bool] = None
    target_hgt: Optional[TargetHgt] = None
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KihonSequence.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KihonSequence':
        return KihonSequence(
            id_sequence=row[0],
            inventory_id=row[1],
            seq_num=row[2],
            stand_id=row[3],
            technic_id=row[4],
            hips=row[5],
            gyaku=row[6],
            target_hgt=row[7],
            resources=row[8],
            notes=row[9],
            resource_url=row[10]
        )

class KihonTx(BaseModel):#get_kihon_tx()
    id_tx: int
    from_sequence: int
    to_sequence: int
    movement: Optional[Movements] = None
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    tempo: Optional[Tempo] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KihonTx.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KihonTx':
        return KihonTx(
            id_tx=row[0],
            from_sequence=row[1],
            to_sequence=row[2],
            movement=row[3],
            resources=row[4],
            notes=row[5],
            tempo=row[6],
            resource_url=row[7]
        )   

class KihonStep(BaseModel): #get_kihon_steps()
    id_sequence: int
    inventory_id: int
    seq_num: int
    stand_id: int
    technic_id: int
    gyaku: bool | None
    target_hgt: TargetHgt | None
    notes: str | None
    resource_url: str | None
    stand_name: str | None
    technic_name: str | None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KihonStep.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KihonStep':
        return KihonStep(
            id_sequence=row[0],
            inventory_id=row[1],
            seq_num=row[2],
            stand_id=row[3],
            technic_id=row[4],
            gyaku=row[5],
            target_hgt=row[6],
            notes=row[7],
            resource_url=row[8],
            stand_name=row[9],
            technic_name=row[10]
        )

class KihonFormatted(BaseModel): #kihon_frmlist()
    number: int
    seq_num: int
    movement: Movements | None
    technic_id: int
    gyaku: bool | None
    tecnica: str | None
    stand_id: int
    posizione: str | None
    target_hgt: TargetHgt | None
    notes: str | None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KihonFormatted.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KihonFormatted':
        return KihonFormatted(
            number=row[0],
            seq_num=row[1],
            movement=row[2],
            technic_id=row[3],
            gyaku=row[4],
            tecnica=row[5],
            stand_id=row[6],
            posizione=row[7],
            target_hgt=row[8],
            notes=row[9]
        )


class KataInventory(BaseModel): # ski.kata_inventory() , public.show_katainventory(), public.get_katainfo()
    id_kata: int
    kata: str
    serie: Optional[KataSeries] = None
    starting_leg: Sides
    notes: Optional[str] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataInventory.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataInventory':
        return KataInventory(
            id_kata=row[0],
            kata=row[1],
            serie=row[2],
            starting_leg=row[3],
            notes=row[4],
            resources=row[5],
            resource_url=row[6]
        )

class KataSequence(BaseModel):
    id_sequence: int
    kata_id: int
    seq_num: int
    stand_id: int
    speed: Optional[Tempo] = None
    side: Optional[Sides] = None
    hips: Optional[Hips] = None
    embusen: Optional[EmbusenPoints] = None
    facing: Optional[AbsoluteDirections] = None
    kiai: Optional[bool] = None
    notes: Optional[str] = None
    remarks: Optional[List[DetailedNotes]] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataSequence.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataSequence':
        return KataSequence(
            id_sequence=row[0],
            kata_id=row[1],
            seq_num=row[2],
            stand_id=row[3],
            speed=row[4],
            side=row[5],
            hips=row[6],
            embusen=row[7],
            facing=row[8],
            kiai=row[9],
            notes=row[10],
            remarks=row[11],
            resources=row[12],
            resource_url=row[13]
        )

class KataSequenceWaza(BaseModel):
    id_kswaza: int
    sequence_id: Optional[int] = None
    arto: Optional[BodyPart] = None
    technic_id: int
    strikingpart_id: Optional[int] = None
    technic_target_id: Optional[int] = None
    notes: Optional[str] = None
    resources: Optional[Dict[str, Any]] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataSequenceWaza.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataSequenceWaza':
        return KataSequenceWaza(
            id_kswaza=row[0],
            sequence_id=row[1],
            arto=row[2],
            technic_id=row[3],
            strikingpart_id=row[4],
            technic_target_id=row[5],
            notes=row[6],
            resources=row[7]
        )

class KataTx(BaseModel):
    id_tx: int
    from_sequence: int
    to_sequence: int
    tempo: Optional[Tempo] = None
    direction: Optional[Sides] = None
    intermediate_stand_id: Optional[int] = None
    notes: Optional[str] = None
    remarks: Optional[List[DetailedNotes]] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataTx.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataTx':
        return KataTx(
            id_tx=row[0],
            from_sequence=row[1],
            to_sequence=row[2],
            tempo=row[3],
            direction=row[4],
            intermediate_stand_id=row[5],
            notes=row[6],
            remarks=row[7],
            resources=row[8],
            resource_url=row[9]
        )

class KataTechnique(BaseModel): #json in tecniche di KataSequenceStep
    sequence_id: int
    arto: BodyPart
    technic_id: int
    Tecnica: str | None = Field(alias="tecnica")
    technic_target_id: int | None
    Obiettivo: str | None = Field(alias="obiettivo")
    waza_note: str | None
    waza_resources: dict | None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataTechnique.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataTechnique':
        return KataTechnique(
            sequence_id=row[0],
            arto=row[1],
            technic_id=row[2],
            tecnica=row[3],
            technic_target_id=row[4],
            obiettivo=row[5],
            waza_note=row[6],
            waza_resources=row[7]
        )

class KataSequenceStep(BaseModel): #get_katasequence()
    id_sequence: int
    kata_id: int
    seq_num: int
    stand_id: int
    posizione: str | None
    guardia: Sides | None
    facing: AbsoluteDirections | None
    Tecniche: List[KataTechnique] = Field(alias="tecniche")
    embusen: EmbusenPoints | None
    kiai: bool | None
    notes: str | None
    remarks: List[DetailedNotes] | None
    resources: dict | None
    resource_url: str | None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataSequenceStep.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataSequenceStep':
        return KataSequenceStep(
            id_sequence=row[0],
            kata_id=row[1],
            seq_num=row[2],
            stand_id=row[3],
            posizione=row[4],
            guardia=row[5],
            facing=row[6],
            tecniche=row[7],
            embusen=row[8],
            kiai=row[9],
            notes=row[10],
            remarks=row[11],
            resources=row[12],
            resource_url=row[13]
        )


class BunkaiInventory(BaseModel): # ski.bunkai_inventory() , public.get_katabunkais()
    id_bunkai: int
    kata_id: int
    version: Optional[int] = 1
    name: str
    description: Optional[str] = None
    notes: Optional[str] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in BunkaiInventory.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'BunkaiInventory':
        return BunkaiInventory(
            id_bunkai=row[0],
            kata_id=row[1],
            version=row[2],
            name=row[3],
            description=row[4],
            notes=row[5],
            resources=row[6],
            resource_url=row[7]
        )

class BunkaiSequence(BaseModel):
    id_bunkaisequence: int
    bunkai_id: int
    kata_sequence_id: int
    description: Optional[str] = None
    notes: Optional[str] = None
    remarks: Optional[List[DetailedNotes]] = None
    resources: Optional[Dict[str, Any]] = None
    resource_url: Optional[str] = None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in BunkaiSequence.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'BunkaiSequence':
        return BunkaiSequence(
            id_bunkaisequence=row[0],
            bunkai_id=row[1],
            kata_sequence_id=row[2],
            description=row[3],
            notes=row[4],
            remarks=row[5],
            resources=row[6],
            resource_url=row[7]
        )