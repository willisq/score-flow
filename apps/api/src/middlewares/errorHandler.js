/**
 * Middleware de manejo de errores centralizado.
 * Debe registrarse DESPUÉS de todas las rutas y otros middlewares en app.js.
 * @param {Error} err - El objeto de error.
 * @param {import('express').Request} req - El objeto de solicitud de Express.
 * @param {import('express').Response} res - El objeto de respuesta de Express.
 * @param {import('express').NextFunction} next - La función para pasar al siguiente middleware.
 */
export const errorHandler = (err, req, res, next) => {
	// Loguear el error para depuración (puedes usar un logger más sofisticado como Winston o Pino)
	console.error(err.stack);

	// Enviar una respuesta genérica de error al cliente
	res.status(500).json({ error: "Ocurrió un error inesperado en el servidor." });
};