import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def model_egit():
    df = pd.read_csv("data/veri_seti.csv")
    X = df.drop(columns = ["dosya_adi","etiket"])
    y = df["etiket"]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    basari_orani = model.score(X_test, y_test)
    print(f"Yapay zeka modeli basari orani: %{basari_orani * 100:.2f}")
    joblib.dump(model, "data/model.pkl")
    print("Model kaydedildi: 'data/model.pkl'")

   
if __name__ == "__main__":
    print("Model egitimi basliyor...")
    model_egit()
