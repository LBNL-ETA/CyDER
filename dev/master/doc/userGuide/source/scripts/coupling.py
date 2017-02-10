from pyfmi import load_fmu
from pyfmi.master import Master

def simulate_multiple_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
        
    """
    cymdist=load_fmu("CYMDIST.fmu", log_level=7)
    gridyn=load_fmu("GridDyn.fmu", log_level=7)
    
    models = [cymdist, gridyn]
    connections = [(gridyn, "VMAG_A", cymdist, "VMAG_A"),
                   (gridyn, "VMAG_B", cymdist, "VMAG_B"),
                   (gridyn, "VMAG_C", cymdist, "VMAG_C"),
                   (gridyn, "VANG_A", cymdist, "VANG_A"),
                   (gridyn, "VANG_B", cymdist, "VANG_B"),
                   (gridyn, "VANG_C", cymdist, "VANG_C"),
                   (cymdist, "KWA_800032440", gridyn, "KWA_800032440"),
                   (cymdist, "KWB_800032440", gridyn, "KWB_800032440"),
                   (cymdist, "KWC_800032440", gridyn, "KWC_800032440"),
                   (cymdist, "KVARA_800032440", gridyn, "KVARA_800032440"),
                   (cymdist, "KVARB_800032440", gridyn, "KVARB_800032440"),
                   (cymdist, "KVARC_800032440", gridyn, "KVARC_800032440"),]
    
    coupled_simulation = Master (models, connections)

    opts=coupled_simulation.simulate_options()
    opts['step_size']=1.0
    opts['logging']=True

    res=coupled_simulation.simulate(options=opts, 
                            start_time=0.0, 
                            final_time=1.0)
        
if __name__ == '__main__':
    simulate_multiple_fmus()
