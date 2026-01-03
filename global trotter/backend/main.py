from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import os
import shutil

# ================== INIT ==================
app = FastAPI(title="GlobalTrotter Backend")

models.Base.metadata.create_all(bind=engine)

# ================== UPLOAD DIRS ==================
UPLOAD_BASE = "uploads"
PROFILE_DIR = "uploads/profiles"
TRIP_DIR = "uploads/trips"
ACTIVITY_DIR = "uploads/activities"
POST_DIR = "uploads/posts"

for d in [UPLOAD_BASE, PROFILE_DIR, TRIP_DIR, ACTIVITY_DIR, POST_DIR]:
    os.makedirs(d, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ================== DB ==================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================== ROOT ==================
@app.get("/")
def root():
    return {"message": "GlobalTrotter Backend Running"}

# =================================================
# ================== AUTH =========================
# =================================================
@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    print("STEP 1: REGISTER HIT")

    # ---------- IMAGE ----------
    img_path = None
    if image:
        print("STEP 2: IMAGE RECEIVED", image.filename)
        try:
            os.makedirs("uploads/profiles", exist_ok=True)
            img_path = f"uploads/profiles/{email}_{image.filename}"

            with open(img_path, "wb") as f:
                shutil.copyfileobj(image.file, f)

            image.file.close()
            print("STEP 3: IMAGE SAVED", img_path)

        except Exception as e:
            print("IMAGE ERROR:", e)
            raise HTTPException(status_code=500, detail="Image upload failed")

    # ---------- DB ----------
    try:
        print("STEP 4: INSERTING USER")

        user = models.User(
            name=name,
            email=email,
            password=password,
            profile_image=img_path
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("STEP 5: USER SAVED")

    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Register success",
        "image": img_path
    }

# =================================================
# ================== TRIP =========================
# =================================================
@app.post("/create-trip")
def create_trip(
    user_id: int = Form(...),
    title: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    status: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    img_path = None
    if image:
        try:
            img_path = f"{TRIP_DIR}/{user_id}_{image.filename}"
            with open(img_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
            image.file.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Trip image upload failed")

    trip = models.Trip(
        user_id=user_id,
        title=title,
        start_date=start_date,
        end_date=end_date,
        status=status,
        cover_image=img_path
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    return {"message": "Trip created", "trip_id": trip.id}

@app.get("/trips/{user_id}")
def get_trips(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Trip).filter(models.Trip.user_id == user_id).all()

# =================================================
# ================== ACTIVITY =====================
# =================================================
@app.post("/add-activity")
def add_activity(
    city: str = Form(...),
    activity_type: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    img_path = None
    if image:
        try:
            img_path = f"{ACTIVITY_DIR}/{city}_{image.filename}"
            with open(img_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
            image.file.close()
        except Exception:
            raise HTTPException(status_code=500, detail="Activity image upload failed")

    act = models.Activity(
        city=city,
        activity_type=activity_type,
        name=name,
        description=description,
        price=price,
        image=img_path
    )
    db.add(act)
    db.commit()

    return {"message": "Activity added"}

@app.get("/activities")
def get_activities(city: str, db: Session = Depends(get_db)):
    return db.query(models.Activity).filter(models.Activity.city == city).all()

# =================================================
# ================== COMMUNITY ====================
# =================================================
@app.post("/community-post")
def community_post(
    user_id: int = Form(...),
    trip_id: int = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    img_path = None
    if image:
        try:
            img_path = f"{POST_DIR}/{user_id}_{image.filename}"
            with open(img_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
            image.file.close()
        except Exception:
            raise HTTPException(status_code=500, detail="Post image upload failed")

    post = models.CommunityPost(
        user_id=user_id,
        trip_id=trip_id,
        content=content,
        image=img_path
    )
    db.add(post)
    db.commit()

    return {"message": "Post created"}

@app.get("/community")
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.CommunityPost).all()

# =================================================
# ================== ADMIN ========================
# =================================================
@app.get("/admin/stats")
def admin_stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(models.User).count(),
        "trips": db.query(models.Trip).count(),
        "activities": db.query(models.Activity).count(),
        "posts": db.query(models.CommunityPost).count()
    }
