# SOPlijner

Digitale vervlechting van richtlijn met standard operating procedures; voorstel voor een lerend netwerk.

## Instructies slurm

1. Clone de rep: 
    ```console 
    git clone https://github.com/rubigdata/SOPlijner.git
    ```

2. scp sick_nl folder naar server: 
    ```console 
    scp -r path/to/dir/local/sick_nl username@server:path/to/dest/on/server
    ```

3. Verbind met server dmv ssh: 
    ```console
    ssh username@server
    ```

    (De rest m.u.v. de laatste stap is allemaal op de server)

4. Creëer virtual env in de server (buiten sick_nl folder zodat je het later terug kan sturen zonder deze virtual env): 
    ```console
    virtualenv --no-download ./sopVirtEnv
    ```

5. Activeer de virtualenv: 
    ```console
    source ./sopVirtEnv/bin/activate
    ```

6. Installeer pytorch (dit zorgde voor problemen als het in de requirements.txt stond dus deze deed ik apart): 
    ```console
    pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
    ```

7. cd naar directory met toegang tot requirements.txt (staat in root van sick_nl) en installeer dan alle overige dependencies: 
    ```console
    pip3 install -r path/to/requirements.txt
    ```

8. Creëer shell script in de code folder van de sick_nl directory: 
    ```console
    nano sopalign.sh 
    ```
    en vul in met: 

    ```shell

    #!/bin/bash
    #SBATCH --partition=<partition>
    #SBATCH --gres=gpu:<aantal_gpus>

    python3 main.py
    ```

    de partition verwacht hier simpelweg de naam van de partition (e.g. csedu) en het aantal_gpus is gewoon een integer (e.g. 4)
9. Start sbatch met ongelimiteerde tijd door tijd op 0 te zetten (of geef tijd aan als deze bekend is): 
    ```console
    sbatch --time=0 sopalign.sh
    ```

10. Inspecteer batch met squeue of door te kijken naar de slurm-batch_number.out file

11. Wacht tot termination, en kopieer terug naar lokaal (dit kopiëren duurt vrij lang door de 8 GB aan modellen)
    ```console
    scp -r username@server:path/to/dest/on/server path/to/dir/local/sick_nl
    ```SOPalign: A Tool for Automatic Estimation of Compliance with Medical Guidelines
