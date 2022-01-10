-- upgrade --
CREATE TABLE IF NOT EXISTS "data_clean" (
    "id" VARCHAR(20) NOT NULL  PRIMARY KEY,
    "content" VARCHAR(280) NOT NULL,
    "date" TIMESTAMP NOT NULL,
    "aprox_city" VARCHAR(3) NOT NULL  /* BAQ: BAQ\nBOG: BOG\nCLO: CLO\nCUC: CUC\nLTC: LTC\nMDE: MDE */,
    "clean_content" VARCHAR(280) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_data_clean_content_45e424" ON "data_clean" ("content");
CREATE INDEX IF NOT EXISTS "idx_data_clean_date_dacaf9" ON "data_clean" ("date");
CREATE INDEX IF NOT EXISTS "idx_data_clean_aprox_c_a0e142" ON "data_clean" ("aprox_city");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
