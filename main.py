from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Tugas 1 Integrasi Sistem", description="API untuk mengelola data mahasiswa")

# Model Data objek sesuai ketentuan tugas
class Mahasiswa(BaseModel):
    id: int
    nama: str
    alamat: str
    ipk: float
    semester: int
    hobi: str

class MahasiswaUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None

# Database sementara (Dummy Database dalam memori)
db_mahasiswa = []

# 1. GET: Mengambil semua data mahasiswa
@app.get("/mahasiswa", response_model=List[Mahasiswa])
def get_all_mahasiswa():
    return db_mahasiswa

# 2. GET By ID: Mengambil data mahasiswa berdasarkan ID
@app.get("/mahasiswa/{mhs_id}", response_model=Mahasiswa)
def get_mahasiswa_by_id(mhs_id: int):
    for mhs in db_mahasiswa:
        if mhs.id == mhs_id:
            return mhs
    raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")

# 3. POST: Menambah data mahasiswa baru
@app.post("/mahasiswa", response_model=Mahasiswa)
def create_mahasiswa(mhs: Mahasiswa):
    for existing in db_mahasiswa:
        if existing.id == mhs.id:
            raise HTTPException(status_code=400, detail="ID mahasiswa sudah terdaftar")
    db_mahasiswa.append(mhs)
    return mhs

# 4. PUT: Mengubah data mahasiswa berdasarkan ID
@app.put("/mahasiswa/{mhs_id}", response_model=Mahasiswa)
def update_mahasiswa(mhs_id: int, data_update: MahasiswaUpdate):
    for index, mhs in enumerate(db_mahasiswa):
        if mhs.id == mhs_id:
            updated_data = mhs.dict()
            for key, value in data_update.dict(exclude_unset=True).items():
                updated_data[key] = value
            
            db_mahasiswa[index] = Mahasiswa(**updated_data)
            return db_mahasiswa[index]
            
    raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")

# 5. DELETE: Menghapus data mahasiswa berdasarkan ID
@app.delete("/mahasiswa/{mhs_id}")
def delete_mahasiswa(mhs_id: int):
    for index, mhs in enumerate(db_mahasiswa):
        if mhs.id == mhs_id:
            db_mahasiswa.pop(index)
            return {"message": f"Data mahasiswa dengan ID {mhs_id} berhasil dihapus"}
            
    raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
from fastapi.responses import RedirectResponse

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")