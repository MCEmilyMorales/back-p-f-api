/*
  Warnings:

  - You are about to drop the column `nombre` on the `Usuario` table. All the data in the column will be lost.
  - You are about to drop the column `password` on the `Usuario` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "Usuario_nombre_key";

-- AlterTable
ALTER TABLE "Usuario" DROP COLUMN "nombre",
DROP COLUMN "password";
