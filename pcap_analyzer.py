import pyshark
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import os

app = Dash(__name__)

PCAP_DIR = "/var/log/pcaps"  # 替換為你的 .pcap 儲存路徑

pcap_files = [f for f in os.listdir(PCAP_DIR) if f.endswith(('.pcap', '.pcapng'))]
if not pcap_files:
    raise ValueError(f"No .pcap or .pcapng files found in {PCAP_DIR}. Please add files or check the directory.")

default_pcap = os.path.join(PCAP_DIR, pcap_files[0])

app.layout = html.Div([
    html.H1("PCAP Analyzer"),
    dcc.Dropdown(
        id='pcap-file',
        options=[{'label': f, 'value': os.path.join(PCAP_DIR, f)} for f in pcap_files],
        value=default_pcap,
        placeholder="Select a PCAP file to analyze"
    ),
    dcc.Graph(id='protocol-pie'),
    html.Pre(id='log-output'),
    html.A(html.Button("Download Log"), href="/download", id="download-link")
])

@app.callback(
    [Output('protocol-pie', 'figure'),
     Output('log-output', 'children'),
     Output('download-link', 'href')],
    [Input('pcap-file', 'value')]
)
def update_graph(pcap):
    if not pcap:
        return px.pie(), "No file selected.", "/download"

    try:
        cap = pyshark.FileCapture(pcap)
        protocols = [pkt.highest_layer for pkt in cap]
        counts = {p: protocols.count(p) for p in set(protocols)}
        
        fig = px.pie(names=list(counts.keys()), values=list(counts.values()), title="Protocol Distribution",
                     color_discrete_sequence=px.colors.qualitative.Set3)  # 漂亮的配色
        log = "\n".join([f"Time: {pkt.sniff_time} | Src: {pkt.ip.src} | Dst: {pkt.ip.dst}" for pkt in cap if hasattr(pkt, 'ip')])
        
        with open("temp_log.txt", "w") as f:
            f.write(log)
        return fig, log, "/download/temp_log.txt"
    
    except Exception as e:
        return px.pie(), f"Error loading {pcap}: {str(e)}", "/download"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8060)
