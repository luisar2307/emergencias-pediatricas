import sys, os
sys.path.insert(0, os.getcwd())
print('cwd', os.getcwd())
print('python', sys.executable)
try:
    import patients
    print('patients package:', patients.__file__)
    import patients.serializers as s
    print('serializers file:', s.__file__)
    print('has PacienteCreateUpdateSerializer:', hasattr(s, 'PacienteCreateUpdateSerializer'))
    if hasattr(s, 'PacienteCreateUpdateSerializer'):
        print('class object:', s.PacienteCreateUpdateSerializer)
    print('Paciente names:', [n for n in dir(s) if 'Paciente' in n])
except Exception as e:
    import traceback
    traceback.print_exc()
