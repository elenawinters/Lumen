const fs = require('node:fs');

const crash_dir = './crash'
if (!fs.existsSync(crash_dir)){
	fs.mkdirSync(crash_dir);
}

process.on('uncaughtException', (err: Error) => {
	console.error('An unexpected and uncaught exception occured. Here are the details of the exception. The process will promptly exit:\n ', err, '\n');
	fs.writeFileSync(
		`${crash_dir}/${Date.now()}.txt`,
		err.stack);
	process.exit();
});

process.on('exit', (code: Number) => {
	console.log('Exited with status code:', code);
});
