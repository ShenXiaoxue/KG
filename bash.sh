gunicorn --bind=127.0.0.1:5000 "digitaltwin:create_app()" #& docker run --rm -v $(pwd)/digitaltwin/library/fenicsx/shared/ -w /root/shared dolfinx/dolfinx:stable "python3 three_floor_FEM_ModalAnalysis.py"

# & docker run --rm -v $(pwd):/home/digitaltwin/library/fenicsx/shared -w /home/digitaltwin/library/fenicsx/shared dolfinx/dolfinx:stable "python3 three_floor_FEM_ModalAnalysis.py"

#python ./digitaltwin/library/fenicsx/three_floor_FEM_ModalAnalysis.py

