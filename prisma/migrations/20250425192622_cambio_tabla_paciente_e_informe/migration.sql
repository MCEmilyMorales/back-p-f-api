/*
  Warnings:

  - You are about to drop the column `num_historia_clinica` on the `Paciente` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "Informe" ADD COLUMN     "promedio_rta_img" TEXT;

-- AlterTable
ALTER TABLE "Paciente" DROP COLUMN "num_historia_clinica",
ADD COLUMN     "dni" TEXT,
ADD COLUMN     "fecha_de_nacimiento" TEXT,
ADD COLUMN     "sexo" TEXT;
