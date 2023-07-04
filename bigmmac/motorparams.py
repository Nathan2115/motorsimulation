
""" Notorious FRC brushed motor, the CIM. Parameters hodge-podged from various Chief Delphi threads."""
cim = {
    'kr': 0.0185,       # Torque/back-EMF constant (N-m/A) or (V-s/rad)
    'Ra': 0.091,        # Armature resistance (ohm)
    'La': 59e-6,        # Armature inductance (H)
    'Jr': 0.000075,     # Motor inertia (kg-m^2)
    'B': 9e-5,          # Motor damping coefficient (N-m-s/rad)
    'Tl': 0,            # Load torque
    'Tf': 0.05          # Dry friction torque
}