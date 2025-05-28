/*
  Warnings:

  - Made the column `promedio_rta_img` on table `Informe` required. This step will fail if there are existing NULL values in that column.
  - Made the column `dni` on table `Paciente` required. This step will fail if there are existing NULL values in that column.
  - Made the column `fecha_de_nacimiento` on table `Paciente` required. This step will fail if there are existing NULL values in that column.
  - Made the column `sexo` on table `Paciente` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "Informe" ALTER COLUMN "promedio_rta_img" SET NOT NULL;

-- AlterTable
ALTER TABLE "Paciente" ALTER COLUMN "dni" SET NOT NULL,
ALTER COLUMN "fecha_de_nacimiento" SET NOT NULL,
ALTER COLUMN "sexo" SET NOT NULL;
