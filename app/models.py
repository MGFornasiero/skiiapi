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
    limb: Limbs | None = None
    side: Sides | None = None

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
    def get_id(self) -> int:
        return self.id_target



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
    def get_id(self) -> int:
        return self.id_part

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
    def get_id(self) -> int:
        return self.id_technic


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
    def get_id(self) -> int:
        return self.id_decomposition




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
    def get_id(self) -> int:
        return self.id_stand

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
    def get_id(self) -> int:
        return self.id_grade
    
    def presentation(self) -> tuple[int, str]:
        return (self.id_grade, f"{self.grade}° {self.gtype}")


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
    def get_id(self) -> int:
        return self.id_inventory


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
    looking_direction: Optional[AbsoluteDirections] = None  # New field
        
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
            resource_url=row[10],
            looking_direction=row[11]  # Add new field
        )
    def get_id(self) -> int:
        return self.id_sequence



class KihonTx(BaseModel):#get_kihon_tx()
    id_tx: int
    from_sequence: int
    to_sequence: int
    movement: Optional[Movements] = None
    resources: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    tempo: Optional[Tempo] = None
    resource_url: Optional[str] = None
    looking_direction: Optional[AbsoluteDirections] = None  # New field
        
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
            resource_url=row[7],
            looking_direction=row[8]  # Add new field
        )   
    def get_id(self) -> int:
        return self.id_tx
    def get_to(self) -> int:
        return self.to_sequence
    def get_from(self) -> int:
        return self.from_sequence




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
    def get_id(self) -> int:
        return self.id_sequence

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
    def presentation(self) -> tuple:
        return (self.number, self.seq_num, 
                {"movement":self.movement,
                 "technic_id":self.technic_id,
                 "gyaku":self.gyaku,
                 "tecnica":self.tecnica,
                 "stand_id":self.stand_id,
                 "Stand":self.posizione,
                 "Target":self.target_hgt,
                 "Note":self.notes})


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
    def get_id(self) -> int:
        return self.id_kata
    def inventory(self) -> tuple[str,int]:
        return (self.kata, self.id_kata)

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
    looking_direction: Optional[AbsoluteDirections] = None  # New field
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
            embusen=EmbusenPoints.model_validate(row[7]._asdict()) if row[7] else None,
            facing=row[8],
            looking_direction=row[9],  # Add new field
            kiai=row[10],
            notes=row[11],
            remarks=row[12],
            resources=row[13],
            resource_url=row[14]
        )
    def get_id(self) -> int:
        return self.id_sequence


class KataSequenceWaza(BaseModel):
    id_kswaza: int
    sequence_id: Optional[int] = None
    arto: Optional[BodyPart] = None
    technic_id: int
    strikingpart_id: Optional[int] = None
    technic_target_id: Optional[int] = None
    target_direction: Optional[AbsoluteDirections] = None  # New field
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
            target_direction=row[6],  # Add new field
            notes=row[7],
            resources=row[8]
        )
    def get_id(self) -> int:
        return self.id_kswaza


class KataTx(BaseModel):
    id_tx: int
    from_sequence: int
    to_sequence: int
    tempo: Optional[Tempo] = None
    direction: Optional[Sides] = None
    intermediate_stand_id: Optional[int] = None
    looking_direction: Optional[AbsoluteDirections] = None  # New field
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
            looking_direction=row[6],  # Add new field
            notes=row[7],
            remarks=[
                DetailedNotes.model_validate(
                    {**t._asdict(), 'arto': t.arto._asdict()}
                ) for t in row[8]
            ] if row[8] else None,
            resources=row[9],
            resource_url=row[10]
        )
    def get_id(self) -> int:
        return self.id_tx
    def get_to(self) -> int:
        return self.to_sequence
    def get_from(self) -> int:
        return self.from_sequence



class KataTechnique(BaseModel): #json in tecniche di KataSequenceStep
    #id_kswaza: int # This seems to be missing from the get_katasequence function result
    sequence_id: int
    arto: BodyPart 
    technic_id: int
    tecnica: str | None = Field(alias="Tecnica")
    strikingpart_id: int | None = None
    strikingpart_name: str | None
    technic_target_id: int | None
    target_direction: AbsoluteDirections | None
    obiettivo: str | None = Field(alias="Obiettivo", default=None)
    waza_note: str | None
    waza_resources: dict | None
        
    def to_sql_values(self) -> str:
        values = [format_value(getattr(self, field)) for field in KataTechnique.model_fields]
        return f"({', '.join(values)})"
    def from_sql_row(row: tuple) -> 'KataTechnique':
        return KataTechnique(
            #id_kswaza=row[0],
            sequence_id=row[1],
            arto=row[2],
            technic_id=row[3],
            tecnica=row[4],
            strikingpart_id=row[5],
            strikingpart_name=row[6],
            technic_target_id=row[7],
            target_direction=row[8],
            obiettivo=row[9],
            waza_note=row[10],
            waza_resources=row[11]
        )
    def get_id(self) -> int:
        return self.id_kswaza



class KataSequenceStep(BaseModel): #get_katasequence()
    id_sequence: int
    kata_id: int
    seq_num: int
    stand_id: int
    posizione: str | None
    speed: Tempo | None
    guardia: Sides | None
    hips: Hips | None
    facing: AbsoluteDirections | None
    looking_direction: AbsoluteDirections | None
    Tecniche: List[KataTechnique] = Field(alias="tecniche")
    embusen: EmbusenPoints | None
    kiai: bool | None
    notes: str | None
    remarks: List[DetailedNotes] | None
    resources: dict | None # sistemare il tupo risorse
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
            speed=row[5],
            guardia=row[6],
            hips=row[7],
            facing=row[8],
            looking_direction=row[9],
            tecniche=[KataTechnique.model_validate(t) for t in row[10]] if row[10] else [],
            embusen=EmbusenPoints(x=row[11][0], y=row[11][1]) if row[11] else None,
            kiai=row[12],
            notes=row[13],
            remarks=[
                DetailedNotes.model_validate(
                    {**t._asdict(), 'arto': t.arto._asdict()}
                ) for t in row[14]
            ] if row[14] else None,
            resources= row[15],
            resource_url=row[16]
        )
    def get_id(self) -> int:
        return self.id_sequence




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
    def get_id(self) -> int:
        return self.id_bunkai



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
    def get_id(self) -> int:
        return self.id_bunkaisequence

class TechnicDecomposition(BaseModel):
    id_decomposition: int
    technic_id: int
    component_order: int
    description: Optional[str] = None
    explanations: Optional[str] = None  # Note: matches explanations not explatations
    resources: Optional[Dict[str, Any]] = None
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
            explanations=row[4],
            resources=row[5],
            notes=row[6],
            resource_url=row[7]
        )
    
    def get_id(self) -> int:
        return self.id_decomposition
