/*
  Warnings:

  - The primary key for the `Imagen` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `Informe` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `Paciente` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `Usuario` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - A unique constraint covering the columns `[informeId]` on the table `Imagen` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[pacienteId]` on the table `Informe` will be added. If there are existing duplicate values, this will fail.

*/
-- DropForeignKey
ALTER TABLE "Imagen" DROP CONSTRAINT "Imagen_informeId_fkey";

-- DropForeignKey
ALTER TABLE "Informe" DROP CONSTRAINT "Informe_pacienteId_fkey";

-- AlterTable
ALTER TABLE "Imagen" DROP CONSTRAINT "Imagen_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "informeId" SET DATA TYPE TEXT,
ADD CONSTRAINT "Imagen_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Imagen_id_seq";

-- AlterTable
ALTER TABLE "Informe" DROP CONSTRAINT "Informe_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "pacienteId" SET DATA TYPE TEXT,
ADD CONSTRAINT "Informe_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Informe_id_seq";

-- AlterTable
ALTER TABLE "Paciente" DROP CONSTRAINT "Paciente_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "Paciente_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Paciente_id_seq";

-- AlterTable
ALTER TABLE "Usuario" DROP CONSTRAINT "Usuario_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "Usuario_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Usuario_id_seq";

-- CreateIndex
CREATE UNIQUE INDEX "Imagen_informeId_key" ON "Imagen"("informeId");

-- CreateIndex
CREATE UNIQUE INDEX "Informe_pacienteId_key" ON "Informe"("pacienteId");

-- AddForeignKey
ALTER TABLE "Informe" ADD CONSTRAINT "Informe_pacienteId_fkey" FOREIGN KEY ("pacienteId") REFERENCES "Paciente"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Imagen" ADD CONSTRAINT "Imagen_informeId_fkey" FOREIGN KEY ("informeId") REFERENCES "Informe"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
