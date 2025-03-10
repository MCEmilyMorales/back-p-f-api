-- DropForeignKey
ALTER TABLE "Imagen" DROP CONSTRAINT "Imagen_informeId_fkey";

-- DropForeignKey
ALTER TABLE "Informe" DROP CONSTRAINT "Informe_pacienteId_fkey";

-- DropForeignKey
ALTER TABLE "Paciente" DROP CONSTRAINT "Paciente_usuarioId_fkey";

-- AddForeignKey
ALTER TABLE "Paciente" ADD CONSTRAINT "Paciente_usuarioId_fkey" FOREIGN KEY ("usuarioId") REFERENCES "Usuario"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Informe" ADD CONSTRAINT "Informe_pacienteId_fkey" FOREIGN KEY ("pacienteId") REFERENCES "Paciente"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Imagen" ADD CONSTRAINT "Imagen_informeId_fkey" FOREIGN KEY ("informeId") REFERENCES "Informe"("id") ON DELETE CASCADE ON UPDATE CASCADE;
