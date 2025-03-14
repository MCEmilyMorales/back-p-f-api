/*
  Warnings:

  - You are about to drop the column `numero_informe` on the `Informe` table. All the data in the column will be lost.
  - Added the required column `num_historia_clinica` to the `Paciente` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Informe" DROP COLUMN "numero_informe";

-- AlterTable
ALTER TABLE "Paciente" ADD COLUMN     "num_historia_clinica" TEXT NOT NULL;
