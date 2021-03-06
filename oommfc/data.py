import os
import glob
import oommfc as oc
import oommfodt as oo
import discretisedfield as df
import micromagneticmodel as mm


class Data(mm.Data):
    @property
    def effective_field(self):
        _dict = {"Demag": "Oxs_Demag::Field",
                 "Exchange": "Oxs_UniformExchange::Field",
                 "UniaxialAnisotropy": "Oxs_UniaxialAnisotropy::Field",
                 "Zeeman": "Oxs_FixedZeeman::Field",
                 "Hamiltonian": "Oxs_RungeKuttaEvolve:evolver:Total field"}

        td = oc.TimeDriver()
        td.drive(self.system, derive=_dict[self.cls])

        dirname = os.path.join(self.system.name, "")
        ohf_file = max(glob.iglob("{}*.ohf".format(dirname)),
                       key=os.path.getctime)

        return df.read_oommf_file(ohf_file)

    @property
    def energy(self):
        _dict = {"Demag": "Demag::Energy",
                 "Exchange": "UniformExchange::Energy",
                 "UniaxialAnisotropy": "UniaxialAnisotropy::Energy",
                 "Zeeman": "FixedZeeman:zeeman:Energy",
                 "Hamiltonian": "RungeKuttaEvolve:evolver:Totalenergy"}
        td = oc.TimeDriver()
        td.drive(self.system, derive="energy")

        dirname = os.path.join(self.system.name, "")
        odt_file = max(glob.iglob("{}*.odt".format(dirname)),
                       key=os.path.getctime)

        dt = oo.OOMMFodt(odt_file, replace_headers=False).df

        return dt[_dict[self.cls]][0]

    @property
    def energy_density(self):
        _dict = {"Demag": "Oxs_Demag::Energy density",
                 "Exchange": "Oxs_UniformExchange::Energy density",
                 "UniaxialAnisotropy": ("Oxs_UniaxialAnisotropy::"
                                        "Energy density"),
                 "Zeeman": "Oxs_FixedZeeman:zeeman:Energy density",
                 "Hamiltonian": ("Oxs_RungeKuttaEvolve:evolver:"
                                 "Total energy density")}

        td = oc.TimeDriver()
        td.drive(self.system, derive=_dict[self.cls])

        dirname = os.path.join(self.system.name, "")
        oef_file = max(glob.iglob("{}*.oef".format(dirname)),
                       key=os.path.getctime)

        return df.read_oommf_file(oef_file)
