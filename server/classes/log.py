import os
import sys
import math
import numpy as np

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)


class Log:
    
    def __init__(self, id_logs, link, descricao, id_piloto, data, id_teste, passada, temporada):
        self.id_logs = id_logs
        self.link = link
        self.descricao = descricao
        self.id_piloto = id_piloto
        self.data = data
        self.id_teste = id_teste
        self.passada = passada
        self.temporada = temporada
    
    def Vehicle_Data_Constants(self):
        self.g = 9.78; # Gravity (m/s^2)
        self.rho = 1.225; # Air density (kg/m^3)
        self.L = 1550; # Wheelbase (mm)
        self.tf = 1150; # Front track (mm)
        self.tr = 1150; # Rear track (mm)
        self.Wfl0 = 75*self.g; # Static front left load (N)
        self.Wfr0 = 75*self.g; # Static front right load (N)
        self.Wrl0 = 75*self.g; # Static rear left load (N)
        self.Wrr0 = 75*self.g; # Static rear right load (N)
        self.W = self.Wfl0 + self.Wfr0 + self.Wrl0 + self.Wrr0; # Total static weight (N)
        self.Af = 1.022; # Frontal area (m^2)
        self.df_a = 0.125342269896867; # Downforce interpolation a coefficient (N/(km/h)^2)
        self.df_b = -0.386251459427891; # Downforce interpolation b coefficient (N/(km/h))
        self.drag_a = 0.059135123564896; # Drag interpolation a coefficient (N/(km/h)^2)
        self.drag_b = -0.079993578517214; # Drag interpolation b coefficient (N/(km/h))
        self.rl = 17.8*25.4/2; # Tire loaded radius (mm)
        self.steer_ratio = 0.17975; # Steer ratio
        temp = [1.938, 1.556, 1.348, 1.208, 1.095]
        self.gear_reduction = [3.576*2.111* elemento for elemento in temp] # Gear reductions
    
    def set_data(self):
        reset = self.time[0]
        for tempo in self.time:
            tempo = tempo - reset
        self.rpm[0] = 4000
        self.tps[0] = 0.01
        self.battery_voltage[0] = 14
        self.oil_temp[0] = None
        self.oil_press[0] = None
        self.engine_temp[0] = None
        self.air_temp[0] = 20
        self.lambdas[0] = 1
        self.fuel_flow[0] = 0.01
        self.fuel_press[0] = None
        self.brake_press_f[0] = 0.01
        self.brake_press_r[0] = 0.01
        self.WPS[0] = 0.01
        self.v_diff[0] = 5
        self.v_fl[0] = 5
        self.v_fr[0] = 5
        self.gear[0] = 2
        self.ax[0] = 0.01
        self.ay[0] = 0.01
        reset = self.damp_xfl[0]
        for damp in self.damp_xfl:
            damp = damp - reset
        reset = self.damp_xrl[0]
        for damp in self.damp_xrl:
            damp = damp - reset
        if all(v is None for v in self.v_fl):
            self.v_fl = self.v_diff
        if all(v is None for v in self.v_fr):
            self.v_fr = self.v_diff

    def data_filtering(self):
        for i in range(1, len(self.time)):
            if self.rpm[i] > 16000 or self.rpm[i] <= 2000:
                self.rpm[i] = self.rpm[i - 1]

            if self.v_fl[i] > 130 or self.v_fl[i] <= 0:
                self.v_fl[i] = self.v_fl[i - 1]
        
            if self.v_fr[i] > 130 or self.v_fr[i] <= 0:
                self.v_fr[i] = self.v_fr[i - 1]
        
            if self.v_diff[i] > 130 or self.v_diff[i] <= 0:
                self.v_diff[i] = self.v_diff[i - 1]
        
            if self.gear[i] > 6 or self.gear[i] < 2:
                self.gear[i] = self.gear[i - 1]
        
            if self.brake_press_f[i] > 1000 or self.brake_press_f[i] < 0:
                self.brake_press_f[i] = self.brake_press_f[i - 1]
        
            if self.brake_press_r[i] > 1000 or self.brake_press_r[i] < 0:
                self.brake_press_r[i] = self.brake_press_r[i - 1]
        
            if self.WPS[i] > 160 or self.WPS[i] < -160:
                self.WPS[i] = self.WPS[i - 1]
        
            if self.tps[i] > 100 or self.tps[i] < 0:
                self.tps[i] = self.tps[i - 1]
        
            if self.ax[i] > 3 or self.ax[i] < -3:
                self.ax[i] = self.ax[i - 1]
        
            if self.ay[i] > 3 or self.ay[i] < -3:
                self.ay[i] = self.ay[i - 1]
        
        for i in range(1, len(self.time)):
            if (self.v_fl[i]+self.v_fr[i])/2 < 5 and self.tps[i] < 5:
                self.rpm[i] = None
                self.tps[i] = None
                self.battery_voltage[i] = None
                self.oil_temp[i] = None
                self.oil_press[i] = None
                self.engine_temp[i] = None
                self.air_temp[i] = None
                self.lambdas[i] = None
                self.fuel_press[i] = None
                self.brake_press_f[i] = None
                self.brake_press_r[i] = None
                self.WPS[i] = None
                self.v_diff[i] = None
                self.gear[i] = None
                self.ax[i] = None
                self.ay[i] = None
            if self.v_fl[i] < 5 and self.brake_press_f[i] + self.brake_press_r[i] < 5:
                self.v_fl[i] = None
            if self.v_fr[i] < 5 and self.brake_press_f[i] + self.brake_press_r[i] < 5:
                self.v_fr[i] = None

    def Memory_Allocation(self):

        self.gf_ovr = [None]*len(self.time) #Overall grip factor (G)
        self.gf_corner = [None]*len(self.time) #Cornering grip factor (G)
        self.gf_brake = [None]*len(self.time) #Braking grip factor (G)
        self.gf_traction = [None]*len(self.time) #Traction grip factor (G)
        self.gf_aero = [None]*len(self.time) #Aero grip factor (G)
        self.brake_bias = [None]*len(self.time) #Front brake bias (%)
        self.steer_speed_on = [None]*len(self.time) #On-steer speed (°/s)
        self.steer_speed_off = [None]*len(self.time) #Off-steer speed (°/s)
        self.brake_speed_on= [None]*len(self.time) #On-brake speed (psi/s)
        self.brake_speed_off= [None]*len(self.time) #Off-brake speed (psi/s)
        self.throttle_speed_on = [None]*len(self.time) #On-throttle speed (%/s)
        self.throttle_speed_off = [None]*len(self.time) #Off-throttle speed (%/s)
        self.trail_braking = [0]*len(self.time) #Trail braking
        self.full_throttle = [0]*len(self.time) #Full throttle
        self.steer_throttle = [0]*len(self.time) #Steering + throttle
        self.coasting = [0]*len(self.time) #Coasting (no pedals)
        self.coasting_off_throttle = [0]*len(self.time) #Off-throttle coasting
        self.coasting_off_brake = [0]*len(self.time) #Off-brake coasting
        self.crossing = [0]*len(self.time) #Crossing (both pedals)
        self.driver_inactive = [1]*len(self.time) #Driver inactivity
        self.gear_shifts = 0 #Number of gear shifts
        self.torque = [0]*len(self.time) #Engine torque (Nm)
        self.low_oil_press_filter = [0]*len(self.time) #Low oil pressure filter (bar)
        self.gear_ratio = [None]*len(self.time) #Theoretical gear ratio

    def Math_Channels(self):
        # -----Acceleration Math Channels-----
        a_comb = []
        ggv_q1 = 0
        ggv_q2 = 0
        ggv_q3 = 0
        ggv_q4 = 0
        for i in range(len(self.time)):
            a_comb.append(math.sqrt((self.ax[i]**2) + (self.ay[i]**2)))
            if self.ay[i] > 0 and self.ax[i] > 0:
                ggv_q1 += 1
            if self.ay[i] < 0 and self.ax[i] > 0:
                ggv_q2 += 1
            if self.ay[i] < 0 and self.ax[i] < 0:
                ggv_q3 += 1
            if self.ay[0] > 0 and self.ax[0] < 0:
                ggv_q4 += 1
        self.ggv_q1 = 100/len(self.time) * ggv_q1 # Percentage of points on the 1st quadrant of the GGD (%)
        self.ggv_q2 = 100/len(self.time) * ggv_q2 # Percentage of points on the 2st quadrant of the GGD (%)
        self.ggv_q3 = 100/len(self.time) * ggv_q3 # Percentage of points on the 3st quadrant of the GGD (%)
        self.ggv_q4 = 100/len(self.time) * ggv_q4 # Percentage of points on the 4st quadrant of the GGD (%)
        self.ggv = [ggv_q1, ggv_q2, ggv_q3, ggv_q4] # Vector for bar plot
        self.a_comb = a_comb # Combined acceleration (G)

        # -----Speed & Aero Math Channels------------
        v_front = []
        drag = []
        downforce = []
        for i in range(len(self.time)):
            v_front.append((self.v_fl[i]+self.v_fr[i]) / 2)
            drag.append(self.drag_a[i] * (v_front[i]**2) + self.drag_b[i] * v_front[i])
            downforce.append(self.drag_a[i] * (v_front[i]**2) + self.drag_b[i] * v_front[i])
        self.v_front = v_front
        self.dist = np.trapz(self.time,(self.v_front / 3.6))
        self.drag = drag
        self.downforce = downforce

        # -----Grip Factor Math Channels-------------
        for i in range(len(self.time)):
            if self.a_comb[i] >= 0.8:
                self.gf_ovr[i] = self.a_comb[i] # Overall grip factor (G)

            if abs(self.ay[i]) >= 0.5:
                self.gf_corner[i] = self.a_comb[i] # Cornering grip factor (G)

            if self.ax[i] <= -0.5:
                self.gf_brake[i] = self.a_comb[i] # Braking grip factor (G)

            if self.ax[i] >= 0.2 and abs(self.ay(i)) >= 0.5:
                self.gf_traction[i] = self.a_comb[i] # Traction grip factor (G)

            if self.ay[i] >= 0.5 and self.v_front[i] >= 36:
                self.gf_aero[i] = self.a_comb[i] # Aero grip factor (G)

        # -----US Angle Math Channels--------
        # Corner radius
        R  = []
        for i in range(self.time):
            R.append(math.sqrt(((self.v_front[i]/3.6)**2)/((self.g * self.ay[i])**2)))
        R[0] = 100
        self.R = R #Corner radius (m)
        for i in range(self.time):
            if abs(self.ay(i)) < 0.4:
                self.R[i] = None
            elif self.R[i] < 1.5:
                self.R[i] = 1.5
        delta_wheel = []
        delta_acker = []
        us_angle = []
        us_grad = []
        for i in range(len(self.time)):
            delta_wheel.append(self.steer_ratio[i] * self.WPS[i])
            delta_acker.append(((self.L/self.R[i]))*(180/math.pi*1000))
            us_angle.append(abs(delta_wheel[i]) - delta_acker[i])
            us_grad.append(us_angle[i]/abs(self.ay[i]))
        
        self.delta_wheel = delta_wheel # Average front wheel steering angle (°)
        self.delta_acker = delta_acker # Ackermann angle (°)
        self.us_angle = us_angle # Understeer angle (°)
        self.us_grad = us_grad # Understeer gradient (°/g)

        # -----Driver Math Channels-----------
        # Brake bias
        brake_press_total = []
        k = []
        power = []
        for i in range(len(self.time)):
            brake_press_total.append(self.brake_press_f[i] + self.brake_press_r[i])
            if self.brake_press_f[i] > 30 and self.brake_press_r[i] > 30:
                self.brake_bias[i] = self.brake_press_f[i]/brake_press_total[i]*100 # Front brake bias (%)
        self.brake_press_total = brake_press_total # Total brake pressure (psi)

        # Driving style digital channels
        for i in  range(1,len(self.time)):
            if self.brake_press_total[i] > 50 and abs(self.WPS[i]) > 10:
                self.trail_braking[i] = 1 # Trail braking
            if self.tps[i] > 5 and abs(self.WPS[i]) > 10:
                self.steer_throttle = 1 # Steering + throttle
            if self.tps[i] >= 95:
                self.full_throttle[i] = 1 # Full throttle
            if self.brake_press_total[i] < 50 and self.tps[i] < 5:
                self.coasting[i] = 1 # Coasting (no pedals)
                if self.tps[i-1] >= 5 or self.coasting_off_throttle[i-1] == 1:
                    self.coasting_off_throttle[i] = 1 # Off-throttle coasting
                elif self.brake_press_total[i-1] >= 50 or self.coasting_off_brake[i-1] == 1:
                    self.coasting_off_brake[i] = 1 # Off-brake coasting
            if self.brake_press_total[i] > 50 and self.tps[i] > 5:
                self.crossing[i] = 1 #Crossing (both pedals)
            if self.brake_press_total[i] > 50 or self.tps[i] > 5 or abs(self.WPS[i]) > 10:
                self.driver_inactive[i] = 0 # Driver inactivity

        # Corner curvature
        k = []
        for i in range(len(self.time)):
            k.append(1/self.R[i])
        self.K = k # Corner curvature (1/m)

        # Number of gear shifts
        for i in range(1, len(self.time)):
            if self.gear[i] != self.gear[i-1]:
                self.gear_shifts += 1 # Number of gear shifts

        # -----Engine Math Channels-----------
        power = []
        for i in range(len(self.time)):
            if self.ax[i] > 0:
                self.torque[i] = (self.W[i]*self.ax[i]+self.drag[i]) * self.rl[i]/1000 # Engine torque at the wheel (Nm)
                power.append(self.torque[i]*self.v_front[i]/3.6/self.rl[i]*1000/745.7)
        fuel_consumption = np.trapz(self.time,self.fuel_flow/1000)
        self.fuel_consumption = fuel_consumption # Fuel consumption (kg)
        self.power = power #Engine power at the wheel (hp)

        # -----Gearing Math Channels-----------
        gear_ratio_calc = []
        for i in range(len(self.time)):
            gear_ratio_calc.append((2*math.pi*self.rpm[i])/(self.v_diff[i]/3.6/self.rl[i]*1000))
            if i == 0:
                gear_ratio_calc[i] = 1
            elif gear_ratio_calc[i] > 30:
                gear_ratio_calc[i] = gear_ratio_calc[i-1]
        self.gear_ratio_calc = gear_ratio_calc # Calculated gear ratio

        RPM2 = []
        RPM3 = []
        RPM4 = []
        RPM5 = []
        RPM6 = []
        for i in range(len(self.time)):
            RPM2.append(self.v_diff[0]/3.6*self.gear_reduction(1)/2/math.pi/self.rl[i]*1000*60)
            if RPM2[i] > 12500:
                RPM2[i] = 12500
            RPM3.append(self.v_diff[0]/3.6*self.gear_reduction(2)/2/math.pi/self.rl[i]*1000*60)
            if RPM3[i] > 12500:
                RPM3[i] = 12500
            RPM4.append(self.v_diff[0]/3.6*self.gear_reduction(3)/2/math.pi/self.rl[i]*1000*60)
            if RPM4[i] > 12500:
                RPM4[i] = 12500
            RPM5.append(self.v_diff[0]/3.6*self.gear_reduction(4)/2/math.pi/self.rl[i]*1000*60)
            if RPM5[i] > 12500:
                RPM5[i] = 12500
            RPM6.append(self.v_diff[0]/3.6*self.gear_reduction(5)/2/math.pi/self.rl[i]*1000*60)
            if RPM6[i] > 12500:
                RPM6[i] = 12500
        self.RPM2 = RPM2
        self.RPM3 = RPM3
        self.RPM4 = RPM4
        self.RPM5 = RPM5
        self.RPM6 = RPM6
        gear_ratio = []
        clutch_speed = []
        for i in range(len(self.time)): # Theoretical gear ratio
            if self.gear[i] == 2:
                gear_ratio[i] = self.gear_reduction[1]
            elif self.gear[i] == 3:
                gear_ratio[i] = self.gear_reduction[2]
            elif self.gear[i] == 4:
                gear_ratio[i] = self.gear_reduction[3]
            elif self.gear[i] == 5:
                gear_ratio[i] = self.gear_reduction[4]
            elif self.gear[i] == 6:
                gear_ratio[i] = self.gear_reduction[5]
            clutch_speed.append((self.v_diff[i]/3.6/self.rl[i]/1000)*self.gear_ratio[i]*30/math.pi)
        self.gear_ratio = gear_ratio
        self.clutch_speed = clutch_speed # Clutch speed (RPM)
    
    def Key_Performance_Indicators(self):
        # -----Grip Factor KPIs---------------
        gf_ovr_avg = 0
        gf_corner_avg = 0
        gf_brake_avg = 0
        gf_traction_avg = 0
        gf_aero_avg = 0
        for i in range(len(self.time)):
            if self.gf_ovr[i] != None:
                gf_ovr_avg += self.gf_ovr[i]
            if self.gf_corner[i] != None:
                gf_corner_avg += self.gf_corner[i]
            if self.gf_brake[i] != None:
                gf_brake_avg += self.gf_brake[i]
            if self.gf_traction[i] != None:
                gf_traction_avg += self.gf_traction[i]
            if self.gf_aero[i] != None:
                gf_aero_avg += self.gf_aero[i]
            gf_ovr_avg /= len(self.time)
            gf_corner_avg /= len(self.time)
            gf_brake_avg /= len(self.time)
            gf_traction_avg /= len(self.time)
            gf_aero_avg /= len(self.time)
        self.gf = [gf_ovr_avg, gf_corner_avg, gf_brake_avg, gf_traction_avg, gf_aero_avg]
        self.gf_ovr_avg = gf_ovr_avg
        self.gf_corner_avg = gf_corner_avg
        self.gf_brake_avg = gf_brake_avg
        self.gf_traction_avg = gf_traction_avg
        self.gf_aero_avg = gf_aero_avg

        # -----Speed & Wheelspeed KPIs--------
        v_max = 0
        for i in range(len(self.time)):
            v_max = max(self.v_front)
        self.v_max = v_max
        # -----Stability KPIs-----------------
        us_grad_avg = 0
        for i in range(len(self.time)):
            us_grad_avg += self.us_grad[i]
        us_grad /= len(self.time)
        # -----Driver KPIs--------------------
        # Steering average & speed
        self.steer_diff = np.diff(abs(self.WPS))/np.diff(self.time)
        steer_speed_on_avg = 0
        steer_speed_off_avg = 0
        steer_avg = 0
        for i in range(len(self.steer_diff)):
            if self.steer_diff[i] > 0 and abs(self.WPS[i]) > 10:
                self.steer_speed_on[i] = self.steer_diff[i]
            elif self.steer_diff[i] < 0 and abs(self.WPS[i]) > 10:
                self.steer_speed_off[i] = abs(self.steer_diff[i])

        for i in range(len(self.steer_speed_on)):
            if self.steer_speed_on[i] != None:
                steer_speed_on_avg += self.steer_speed_on[i]

        for i in range(len(self.steer_speed_off_avg)):
            if self.steer_speed_on[i] != None:
                steer_speed_off_avg += self.steer_speed_off[i]

        for i in range(len(self.time)):
            steer_avg += abs(self.WPS[i])

        self.steer_speed_on_avg = steer_speed_on_avg/len(self.steer_speed_on)
        self.steer_speed_off_avg = steer_speed_off_avg/len(self.steer_speed_off)
        self.steer_avg = steer_avg/len(self.WPS)
        # Braking average & speed
        





