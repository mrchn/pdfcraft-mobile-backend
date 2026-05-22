import os, subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.post('/convert')
async def convert_docx_to_pdf(file: UploadFile = File(...)):
	if not file.filename.endswith('.docx'): raise HTTPException(status_code=400, detail='sorry, only .docx')
	input_path = f'/tmp/{file.filename}' ; output_dir = '/tmp'
	pdf_filename = file.filename.replace('.docx', '.pdf')
	output_path = f'/tmp/{pdf_filename}'

	try:
		with open(input_path, 'wb') as f: f.write(await file.read())
		result = subprocess.run([
			'libreoffice', '--headless', '--convert-to', 'pdf',
			'--outdir', output_dir, input_path
		], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		if result.returncode != 0:
			print('libreoffice error:', result.stderr)
			raise HTTPException(status_code=500, detail='libreoffice error')
		return FileResponse(output_path, media_type='application/pdf', filename=pdf_filename)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		if os.path.exists(input_path): os.remove(input_path)
