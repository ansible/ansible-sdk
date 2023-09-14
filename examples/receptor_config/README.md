# Terminal 1
cd <SRC>/ansible-sdk/examples/receptor_config
podman run -it --rm --network host --name foo -v${PWD}/foo.yml:/etc/receptor/receptor.conf -v${PWD}:/receptor_config:Z quay.io/ansible/receptor

# Terminal 2
podman exec -it <CONTAINER_ID> /bin/bash
receptor --config /receptor_config/bar.yml

# Terminal 3
podman exec -it <CONTAINER_ID> /bin/bash
receptor --config /receptor_config/baz.yml

# Terminal 4
podman exec -it <CONTAINER_ID> /bin/bash
mkdir /src
cd /src
git clone https://github.com/ansible/ansible-sdk
cd ansible-sdk
pip3 install -r requirements.txt
pip3 install .
cd examples
python3 example_mesh_job.py

