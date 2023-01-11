import tkinter
from tkinter import *
import sys, os, re
import ctypes
    
class Splash:
    
    def __init__(self, master):
        self.master = master
        self.master.title('SSURGO On-Demand')
        self.frame = tkinter.Frame(self.master)
        f = ("DejaVuSans", 10, "bold")
        
        base = sys.argv[0]
        bDir = os.path.dirname(base)
        ico = os.path.join(bDir, 'ncss.ico')
        png = os.path.join(bDir, 'ncss.png')
        
        try:
        	self.master.iconbitmap(ico)
        
        except:
            
            if os.path.exists(png):
            
                img = tkinter.Image("photo", file=png)
                self.master.tk.call('wm','iconphoto',self.master._w,img)
        
            else:
                pass
        
        dialog = """
        These tools utilize either a SQLite (.sqlite) or Geopackage (.gpkg) database to aggregate soil
        property or interpretation information.  Source data are typically Web Soil Survey - Soil 
        Survey Geographic Database (SSURGO) downloads that have been imported into one of 
        these databases. When properties or interpretations have been executed with this tool 
        the results are tables written to the template database and have a 'SSURGOOnDemand' prefix.
        These tables can be used in GIS software and joined to spatial data using the map unit key
        (mukey) fields.
        
        Soil propeties are attributes found in a soil profile that can be measured or evaluated. 
        Examples include percent sand, percent silt, percent clay, bulk density (g/cm3), 
        available water capacity (cm/cm), etc.
        
        Soil interpretations evaluate soil classes for suitabilty and limitations in land use 
        applications and management. Examples include Dwellings with Basements, Camping Areas, 
        Land Application of Sewage Sludge, Potential Seedling Mortality, etc. Interpretations typically 
        use soil properties to generate the suitability or limitation rating.""" 
        
        
        # intro frame
        self.introFrame = tkinter.LabelFrame(self.frame, text='Generate soil properties and interpretations from SSURGO template databases', font = f)
        self.introFrame.grid(row=0, column=0, padx = 15, pady= 10)
        
        self.propDesc = tkinter.Label(self.introFrame, text=dialog, justify='left')
        self.propDesc.grid(row=0, column=0)
        
        # run frame
        self.runFrame = tkinter.LabelFrame(self.frame, text='Next', font = f)
        self.runFrame.grid(sticky = 'n', row=1, column=0, padx = 15, pady= 10)
        
        self.button1 = tkinter.Button(self.runFrame, text = 'Properties', width = 20, command = self.prop_window)
        self.button1.grid(row=1, column=0, padx=10, pady=10)
        
        self.button1 = tkinter.Button(self.runFrame, text = 'Interpretations', width = 20, command = self.interp_window)
        self.button1.grid(row=1, column=1, padx=10, pady=10)
        
        self.button1 = tkinter.Button(self.runFrame, text = 'Exit', width = 20, command = self.cancel)
        self.button1.grid(row=1, column=2, padx=10, pady=10)
        
        self.frame.pack()

    
    def prop_window(self):
        self.newWindow = tkinter.Toplevel(self.master)
        self.app = Properties(self.newWindow)
    
    
    def interp_window(self):
        self.newWindow = tkinter.Toplevel(self.master)
        self.app = Interpretations(self.newWindow)
        
    
    def cancel(self):
        self.master.destroy()
    

class Properties:
    
    def __init__(self, master):
        self.master = master
        self.master.title('Properties - SSURGO On-Demand')
        self.frame = tkinter.Frame(self.master)
        
        base = sys.argv[0]
        bDir = os.path.dirname(base)
        ico = os.path.join(bDir, 'ncss.ico')
        png = os.path.join(bDir, 'ncss.png')
        
        try:
         	self.master.iconbitmap(ico)
        
        except:
            
            if os.path.exists(png):
            
                img = tkinter.Image("photo", file=png)
                self.master.tk.call('wm','iconphoto',self.master._w,img)
                
            else:
                pass
        
        f = ("DejaVuSans", 10, "bold")
        
        # === select tempalte dbframe
        self.openFrame = tkinter.LabelFrame(self.frame, text='Select Template Database', font=f)
        self.openFrame.grid(sticky = 'w', row=0, column=0, padx = 15, pady= 10)
        self.OpenButton = tkinter.Button(self.openFrame, text="Open", width=10, command=self.openDB)
        self.OpenButton.grid(row=0, padx=10, pady=10)
        
        # === aggregation method frame
        self.methods = ['Weighted Average', 'Dominant Component Numeric', 'Dominant Component Categorical',  'Dominant Condition', 'Minimum/Maximum']
        
        self.aggFrame = tkinter.LabelFrame(self.frame, text='Select Aggregation Method', font=f)
        self.aggFrame.grid(sticky = 'w', row=1, column=0, padx = 15, pady= 10)
        
        self.aggChoices = tkinter.StringVar()
        
        self.aggChoices.trace('r', self.callback)
        
        self.aggChoices.set(self.methods[1])
        self.aggMethod = tkinter.OptionMenu(self.aggFrame, self.aggChoices, *self.methods, command=self.callback)
        self.aggMethod.grid(row=0, column=0, padx=10, pady=10) 
        self.aggSubmit = tkinter.Button(self.aggFrame, text = 'Submit', width = 10,  command=self.propGen)
        self.aggSubmit.grid(row=0, column=1, padx=10, pady=10)
        
        # === soil properties frame         
        self.propFrame = tkinter.LabelFrame(self.frame, text='Select Soil Properties', font=f)
        self.propFrame.grid(sticky = 'w', row=2, column=0, padx = 15, pady= 10)
        
        # === depth frame
        self.depthFrame = tkinter.LabelFrame(self.frame, text='Select Depth Range (*Optional) ', font=f)
        self.depthFrame.grid(sticky='w', row=3, column=0, padx = 15, pady= 10)
        
        self.topLabel = tkinter.Label(self.depthFrame, text = 'Top Depth', font = f)
        self.topLabel.grid(row=0, column = 0, padx=10, pady=10)
        self.topD = tkinter.Entry(self.depthFrame, width = 5)
        self.topD.grid(row = 0, column=1, padx=5)
        
        self.spacer = tkinter.Label(self.depthFrame, text = "   ")
        self.spacer.grid(row=0, column=2, padx=10, pady=10)
        
        self.bottomLabel = tkinter.Label(self.depthFrame, text = 'Bottom Depth', font = f)
        self.bottomLabel.grid(row=0, column=3, padx=10, pady=10)
        self.bottomD = tkinter.Entry(self.depthFrame, width = 5)
        self.bottomD.grid(row = 0, column=4, padx=10)
        
        # === minmax frame
        self.mmL = ['', 'MIN', 'MAX']
        
        self.mmFrame = tkinter.LabelFrame(self.frame, text='Select Minimum or Maximum (*Optional)', font = f)
        self.mmFrame.grid(sticky = 'w', row=4, column=0, padx = 15, pady = 10)

        self.mmChoices = tkinter.StringVar()
        self.mmChoices.set(self.mmL[1])
        self.mmOptions = tkinter.OptionMenu(self.mmFrame, self.mmChoices, *self.mmL)
        self.mmOptions.grid(row=0, column=0, padx=10, pady=10)                           
        
                  
        # === execute frame
        self.runFrame = tkinter.LabelFrame(self.frame, text='Execute', font = f)
        self.runFrame.grid(row=5, column=0, padx = 15, pady = 10)
        
        self.runButton = tkinter.Button(self.runFrame, text = 'Run', width = 20, command = self.run)
        self.runButton.grid(row=0, column=0, padx=10, pady=10)
        self.runButton["activebackground"] = '#d8e1d9'
        
        self.quitButton = tkinter.Button(self.runFrame, text = 'Cancel', width = 20, command = self.close_windows)
        self.quitButton.grid(row=0, column=1, padx=10, pady=10)
        
        self.propGen()
        # self.runState()
        
        self.frame.pack()
        
   
    def openDB(self):
        
        import tkinter.filedialog
        self.db = tkinter.filedialog.askopenfilename(parent=self.frame,  initialdir="", title="Select SSURGO Template Database", filetypes=(("SQLite", " *.gpkg"), ("SQLite", "*.sqlite"), ("All Files", "*")))
        typind = self.db.rfind(".")
        self.dtype = self.db[typind:]
        self.openLbl=tkinter.Label(self.openFrame, text=self.db, bg='white', padx=5, pady=5)
        self.openLbl.grid(sticky = 'w', row=0, column=1)
        
        # return self.db
        
    
    def propGen(self):
        
        global propList
        global catprops
        global numprops
        global minmax
        
        catprops = ['Corrosion of Concrete', 'Corrosion of Steel', 'Drainage Class', 'Hydrologic Group', 'Taxonomic Class Name', 'Taxonomic Order', 'Taxonomic Particle Size', 'Taxonomic Suborder', 'Taxonomic Temperature Regime', 'Wind Erodibility Group', 'Wind Erodibility Index', 't Factor']
        numprops = ['0.1 bar H2O - Rep Value', '0.33 bar H2O - Rep Value', '15 bar H2O - Rep Value', 'Available Water Capacity - Rep Value', 'Bray 1 Phosphate - Rep Value', 'Bulk Density 0.1 bar H2O - Rep Value', 'Bulk Density 0.33 bar H2O - Rep Value', 'Bulk Density 15 bar H2O - Rep Value', 'Bulk Density oven dry - Rep Value', 'CaCO3 Clay - Rep Value', 'Calcium Carbonate - Rep Value', 'Cation Exchange Capcity - Rep Value', 'Coarse Sand - Rep Value', 'Coarse Silt - Rep Value', 'Effective Cation Exchange Capcity - Rep Value', 'Electrical Conductivity - Rep Value', 'Extract Aluminum - Rep Value', 'Extractable Acidity - Rep Value', 'Fine Sand - Rep Value', 'Fine Silt - Rep Value', 'Free Iron - Rep Value', 'Gypsum - Rep Value', 'LEP - Rep Value', 'Liquid Limit - Rep Value', 'Medium Sand - Rep Value', 'Organic Matter - Rep Value', 'Oxalate Aluminum - Rep Value', 'Oxalate Iron - Rep Value', 'Oxalate Phosphate - Rep Value', 'Plasticity Index - Rep Value', 'Rock Fragments 3 - 10 cm - Rep Value', 'Rock Fragments > 10 cm - Rep Value', 'Satiated H2O - Rep Value', 'Saturated Hydraulic Conductivity - Rep Value', 'Sodium Adsorption Ratio - Rep Value', 'Sum of Bases - Rep Value', 'Total Clay - Rep Value', 'Total Phosphate - Rep Value', 'Total Sand - Rep Value', 'Total Silt - Rep Value', 'Very Coarse Sand - Rep Value', 'Very Fine Sand - Rep Value', 'Water Soluble Phosphate - Rep Value', 'no. 10 sieve - Rep Value', 'no. 200 sieve - Rep Value', 'no. 4 sieve - Rep Value', 'no. 40 sieve - Rep Value']
        minmax = ['0.1 bar H2O - Rep Value', '0.33 bar H2O - Rep Value', '15 bar H2O - Rep Value', 'Available Water Capacity - Rep Value', 'Bray 1 Phosphate - Rep Value', 'Bulk Density 0.1 bar H2O - Rep Value', 'Bulk Density 0.33 bar H2O - Rep Value', 'Bulk Density 15 bar H2O - Rep Value', 'Bulk Density oven dry - Rep Value', 'CaCO3 Clay - Rep Value', 'Calcium Carbonate - Rep Value', 'Cation Exchange Capcity - Rep Value', 'Coarse Sand - Rep Value', 'Coarse Silt - Rep Value', 'Effective Cation Exchange Capcity - Rep Value', 'Electrical Conductivity - Rep Value', 'Extract Aluminum - Rep Value', 'Extractable Acidity - Rep Value', 'Fine Sand - Rep Value', 'Fine Silt - Rep Value', 'Free Iron - Rep Value', 'Gypsum - Rep Value', 'Kf', 'Kw ', 'LEP - Rep Value', 'Liquid Limit - Rep Value', 'Medium Sand - Rep Value', 'Organic Matter - Rep Value', 'Oxalate Aluminum - Rep Value', 'Oxalate Iron - Rep Value', 'Oxalate Phosphate - Rep Value', 'Plasticity Index - Rep Value', 'Rock Fragments 3 - 10 cm - Rep Value', 'Rock Fragments > 10 cm - Rep Value', 'Satiated H2O - Rep Value', 'Saturated Hydraulic Conductivity - Rep Value', 'Sodium Adsorption Ratio - Rep Value', 'Sum of Bases - Rep Value', 'Total Clay - Rep Value', 'Total Phosphate - Rep Value', 'Total Sand - Rep Value', 'Total Silt - Rep Value', 'Very Coarse Sand - Rep Value', 'Very Fine Sand - Rep Value', 'Water Soluble Phosphate - Rep Value', 'no. 10 sieve - Rep Value', 'no. 200 sieve - Rep Value', 'no. 4 sieve - Rep Value', 'no. 40 sieve - Rep Value']
        choice = self.callback()
        
        choices = ['', 'Dominant Component Categorical',  'Dominant Condition', 'Minimum/Maximum']
        if choice in choices:
            self.topD.delete(0, 'end')
            self.bottomD.delete(0, 'end')    
            self.disable(self.topD, 'disabled')
            self.disable(self.bottomD, 'disabled')
        else:
            self.disable(self.topD, 'normal')
            self.disable(self.bottomD, 'normal')
        
        if choice == choices[3]:
            self.mmChoices.set(self.mmL[1])
            self.disable(self.mmOptions, 'normal')
        else:
            self.mmChoices.set(self.mmL[0])
            self.disable(self.mmOptions, 'disabled')
            
        self.scrollbar = tkinter.Scrollbar(self.propFrame)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        self.propList = tkinter.Listbox(self.propFrame, selectmode='multiple', width=50)
        self.propList.grid(row=0, padx=10, pady=10)
        self.propList.configure(exportselection=False)
        self.propList.config(exportselection=False)
        # self.propList.grid(row=0, column=0)

        self.propList.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.propList.yview)    
        
        if (choice == 'Dominant Component Categorical') or (choice == 'Dominant Condition'):
            for i,item in enumerate(catprops):
                self.propList.insert(i, item)
        
        elif (choice == 'Weighted Average') or (choice == 'Dominant Component Numeric'):
            # self.propList.delete(0, 'END')
            for i,item in enumerate(numprops):
                self.propList.insert(i, item)
                
        elif choice == 'Minimum/Maximum':
            for i,item in enumerate(minmax):
                self.propList.insert(i, item)
        
    def disable(self, widget, state):
        
        widget.config(state=state)     
    
    
    def callback(self, *args):
        
        choice = self.aggChoices.get()
        return choice
        
    
    def run(self):
        
        # import sys
        message = ''
        
        method = self.callback()
        propInd = self.propList.curselection()
        propRun = ",".join([self.propList.get(i) for i in propInd])
        runTop = self.topD.get()
        runBot = self.bottomD.get()
        
        opt = (method, propInd, propRun, runTop, runBot)
        print(opt)
        
        if not method in ['Dominant Component Categorical',  'Dominant Condition', 'Minimum/Maximum']:
            
            try:
                runTop = int(self.topD.get())
                runBot = int(self.bottomD.get())
                if runTop > runBot:
                    message=('Top depth is greater than bottom depth')
                    # self.invalid(message)
                    
                elif (runTop > 199) or (runBot > 200):
                    message = ("Enter depth ranges between 0 - 200 cm")
                    # self.invalid(message)
                    
                elif (runTop < 0)  or (runBot < 0):
                    message = 'Only positive integer depth values are valid'
                    # self.invalid(message)
                    
            except:
                message='Only positive integer depth values are valid'
                
        
        if propRun == '':
            message = 'Select at least 1 soil property'
            # self.invalid(message)
        
        else:
            propReq = propRun.split(',')
        
        
        if method in ['Dominant Component Categorical',  'Dominant Condition']:
            try:
                if (propReq[0] in numprops) or (propReq[0] in minmax):
                    message = 'Selected aggregation method not valid for requested properties'
                    # self.invalid(message)
            except: 
                message = 'Select at least 1 soil property'
                # self.invalid(message)
        
        else:
            try:
                if propReq[0] in catprops:
                    message = 'Selected aggregation method not valid for requested property(s)'
                    # self.invalid(message)

                if method in ['Weighted Average', 'Dominant Component Numeric']:
                        iv = ['Kf', 'Kw']
                        if any(x in iv for x in propReq):
                            message = 'Selected aggregation method does not support K factor'
            except:
                message = 'Select at least 1 soil property'
                # self.invalid(message)
                
        if method == 'Minimum/Maximum':
            mmGet = self.mmChoices.get()
            if mmGet == '':
                message = 'Select Min or Max aggregation'
                # self.invalid(message=message)

        try:
            
            db = self.openLbl.cget('text')
            print(db)
            if not os.path.isfile(db):
                message = "Unable to locate database"
                # self.invalid(message=messsage)
            else:
                
                count = self.validDB()
                if count < 1:
                    message = 'Databbase does not appear to be a populated SSURGO database'
                    # self.invalid(message)
                
        except:
            message = "Invalid database"
            # self.invalid(message)
        
        if message != '':
            self.invalid(message=message)
            
            
        else:
            # when we get here we should have a set
            # of valid criteria to build a query
            
            if method == 'Dominant Component Categorical':
                
                for p in propReq:
                    sdaCol = self.proplu(p)
                    tQry, pQry = self.dcpc(sdaCol, self.dtype)
                    # print(theQry)
                    self.exeq(tQry)
                    self.exeq(pQry)
            
            elif method == 'Minimum/Maximum':
                
                for p in propReq:
                    sdaCol = self.proplu(p)
                    mmChoice = self.mmChoices.get()
                    tQry, pQry = self.minmax(sdaCol, mmChoice, self.dtype)
                    self.exeq(tQry)
                    self.exeq(pQry)
            
            elif method == 'Dominant Condition':
                
                for p in propReq:
                    sdaCol = self.proplu(p)
                    tQry, pQry = self.dcond(sdaCol, self.dtype)
                    self.exeq(tQry)
                    self.exeq(pQry)
                    
            elif method == 'Weighted Average':
                
                for p in propReq:
                    sdaCol = self.proplu(p)
                    tQry, pQry = self.wtdavg(sdaCol, str(runTop), str(runBot), self.dtype)
                    self.exeq(tQry)
                    self.exeq(pQry)
            
            elif method == 'Dominant Component Numeric':
                
                for p in propReq:
                    sdaCol = self.proplu(p)
                    tQry, pQry = self.dcpn(sdaCol, str(runTop), str(runBot), self.dtype)
                    self.exeq(tQry)
                    self.exeq(pQry)
            
    
    def invalid(self, message):
        from tkinter import messagebox
        mbox = tkinter.messagebox.showerror('Error',  message=message, parent=self.frame)
                
    
    def validDB(self):
        
        q = """SELECT COUNT(*) FROM sacatalog;"""
        sacount = self.exeq(q, kind='select')
        return sacount
                
        
    def dcpc(self, col, dbtype):
        
        tblname = 'SSURGOOnDemand_dom_comp_' + col
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;"""
        
        qry_dcpc = """--dominant component categorical
        CREATE TABLE """ + tblname + """ AS SELECT areasymbol, musym, muname, compname, comppct_r, mu.mukey  AS mukey,""" + col + """ AS """ + col + """
        FROM legend  AS l
        INNER JOIN  mapunit AS mu ON mu.lkey = l.lkey
        INNER JOIN component AS c ON c.mukey = mu.mukey
        AND c.cokey =
        (SELECT c1.cokey FROM component AS c1
        INNER JOIN mapunit ON c.mukey=mapunit.mukey AND c1.mukey=mu.mukey ORDER BY c1.comppct_r DESC, c1.cokey LIMIT 1);
        """
        
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_dcpc = qry_dcpc + gcontents

        else:
            pass            
        
        # print(test)
        # print(qry_dcpc)
        return test, qry_dcpc
    
    
    def minmax(self, col, mmc, dbtype):
        
        tblname = 'SSURGOOnDemand_minmax_' + col + '_' + mmc
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;"""
        
        qry_mm = """--minimum/maximum
        CREATE TABLE """ + tblname + """ AS SELECT areasymbol, musym, muname, mu.mukey  AS mukey,
        (SELECT CAST(""" + mmc + """ (chm1.""" + col + """) AS REAL) FROM  component AS cm1
        INNER JOIN chorizon AS chm1 ON cm1.cokey = chm1.cokey AND cm1.cokey = c.cokey AND majcompflag = 'Yes'
        AND CASE WHEN chm1.hzname LIKE  '%O%' AND hzdept_r <10 THEN 2
        WHEN chm1.hzname LIKE  '%r%' THEN 2
        WHEN chm1.hzname LIKE  '%'  THEN  1 ELSE 1 END = 1
        LIMIT 1) AS """ + col + """
        FROM legend  AS l
        INNER JOIN  mapunit AS mu ON mu.lkey = l.lkey
        INNER JOIN  component AS c ON c.mukey = mu.mukey AND majcompflag = 'Yes' AND c.cokey =
        (SELECT c1.cokey FROM component AS c1
        INNER JOIN mapunit ON c.mukey=mapunit.mukey AND c1.mukey=mu.mukey ORDER BY c1.comppct_r DESC, c1.cokey LIMIT 1);
        """
        
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_mm = qry_mm + gcontents

        else:
            pass            
        
        print(qry_mm)
        return test, qry_mm
    
    
    def dcond(self, col, dbtype):
        
        tblname = 'SSURGOOnDemand_dom_cond_' + col
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;"""
        
        qry_dcon = """--dominant condition
        CREATE TABLE """ + tblname + """ AS SELECT areasymbol, musym, muname, mu.mukey/1  AS mukey,
        (SELECT """ + col + """
        FROM mapunit
        INNER JOIN component ON component.mukey=mapunit.mukey
        AND mapunit.mukey = mu.mukey
        GROUP BY """ + col + """, comppct_r ORDER BY SUM(comppct_r) over(partition by hydgrp) DESC LIMIT 1) AS """ + col + """
        FROM legend  AS l
        INNER JOIN  mapunit AS mu ON mu.lkey = l.lkey
        INNER JOIN  component AS c ON c.mukey = mu.mukey
        AND c.cokey =
        (SELECT c1.cokey FROM component AS c1
        INNER JOIN mapunit ON c.mukey=mapunit.mukey AND c1.mukey=mu.mukey ORDER BY c1.comppct_r DESC, c1.cokey LIMIT 1)
        GROUP BY areasymbol, musym, muname, mu.mukey, c.cokey,  compname, comppct_r
        ORDER BY areasymbol, musym, muname, mu.mukey, comppct_r DESC, c.cokey """
        
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_dcon = qry_dcon + gcontents

        else:
            pass            
        
        return test, qry_dcon
    
    
    def wtdavg(self, col, tDep, bDep, dbtype):
        
        tblname = 'SSURGOOnDemand_wtd_avg_' + col + '_' + tDep + '_' + bDep
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;"""
        
        qry_wtdavg = """--weighted average
        
        DROP TABLE IF EXISTS kitchensink;
        DROP TABLE IF EXISTS comp_temp;
        DROP TABLE IF EXISTS comp_temp2;
        DROP TABLE IF EXISTS comp_temp3;
        DROP TABLE IF EXISTS last_step;
        DROP TABLE IF EXISTS last_step2;
        DROP TABLE IF EXISTS temp_main;
        
        CREATE TABLE kitchensink AS
        SELECT areasymbol, musym, muname, mukey
        FROM legend  AS lks
        INNER JOIN  mapunit AS muks ON muks.lkey = lks.lkey;  
        
        CREATE TABLE comp_temp AS		
        SELECT mu1.mukey, cokey, comppct_r,
        SUM (comppct_r) over(partition by mu1.mukey ) AS SUM_COMP_PCT
        FROM kitchensink AS mu1
        INNER JOIN  component AS c1 ON c1.mukey = mu1.mukey AND majcompflag = 'Yes';	
        
        CREATE TABLE comp_temp3 AS
        SELECT cokey, SUM_COMP_PCT, CASE WHEN comppct_r = SUM_COMP_PCT THEN 1
        ELSE CAST (CAST (comppct_r AS  REAL) / CAST (SUM_COMP_PCT AS REAL) AS REAL) END AS WEIGHTED_COMP_PCT
        FROM comp_temp;	
        
        CREATE TABLE temp_main AS		
        SELECT
        areasymbol, musym, muname, mu.mukey/1  AS MUKEY, c.cokey AS COKEY, ch.chkey/1 AS CHKEY, compname, hzname, hzdept_r, hzdepb_r, CASE WHEN hzdept_r < """ + tDep + """  THEN 0 ELSE hzdept_r END AS hzdept_r_ADJ,
        CASE WHEN hzdepb_r > """ + bDep + """  THEN 100 ELSE hzdepb_r END AS hzdepb_r_ADJ,
        CAST (CASE WHEN hzdepb_r > """ + bDep + """  THEN 100 ELSE hzdepb_r END - CASE WHEN hzdept_r < """ + tDep + """ THEN 0 ELSE hzdept_r END AS decimal (5,2)) AS thickness,
        comppct_r,
        CAST (SUM (CASE WHEN hzdepb_r > """ + bDep + """  THEN 100 ELSE hzdepb_r END - CASE WHEN hzdept_r < """ + tDep + """ THEN 0 ELSE hzdept_r END) over(partition by c.cokey) AS decimal (5,2)) AS sum_thickness,
        CAST (IFNULL (""" + col + """, 0) AS REAL) AS """ + col + """
        
        FROM kitchensink AS mu
        INNER JOIN  component AS c ON c.mukey = mu.mukey AND majcompflag = 'Yes'
        INNER JOIN chorizon AS ch ON ch.cokey=c.cokey AND hzname NOT LIKE '%O%'AND hzname NOT LIKE '%r%'
        AND hzdepb_r > """ + tDep + """ AND hzdept_r < """ + bDep + """
        INNER JOIN chtexturegrp AS cht ON ch.chkey=cht.chkey  WHERE cht.rvindicator = 'Yes' AND  ch.hzdept_r IS NOT NULL
        AND texture NOT LIKE '%PM%' and texture NOT LIKE '%DOM' and texture NOT LIKE '%MPT%' and texture NOT LIKE '%MUCK' and texture NOT LIKE '%PEAT%' and texture NOT LIKE '%br%' and texture NOT LIKE '%wb%'
        ORDER BY areasymbol, musym, muname, mu.mukey, comppct_r DESC, cokey,  hzdept_r, hzdepb_r	;	
        
        CREATE TABLE comp_temp2 AS 
        SELECT temp_main.areasymbol, temp_main.musym, temp_main.muname, temp_main.MUKEY,
        temp_main.COKEY, temp_main.CHKEY, temp_main.compname, hzname, hzdept_r, hzdepb_r, hzdept_r_ADJ, hzdepb_r_ADJ, thickness, sum_thickness, """ + col + """, comppct_r, SUM_COMP_PCT, WEIGHTED_COMP_PCT ,
        SUM((CAST (thickness  AS REAL )/CAST (sum_thickness  AS REAL ) ) * """ + col + """ )over(partition by temp_main.COKEY)AS COMP_WEIGHTED_AVERAGE
        FROM temp_main
        INNER JOIN comp_temp3 ON comp_temp3.cokey=temp_main.cokey
        ORDER BY temp_main.areasymbol, temp_main.musym, temp_main.muname, temp_main.MUKEY, comppct_r DESC,  temp_main.COKEY,  hzdept_r, hzdepb_r;
        
        CREATE TABLE last_step AS 
        SELECT comp_temp2.MUKEY,comp_temp2.COKEY, WEIGHTED_COMP_PCT * COMP_WEIGHTED_AVERAGE AS COMP_WEIGHTED_AVERAGE1
        FROM comp_temp2
        GROUP BY  comp_temp2.MUKEY,comp_temp2.COKEY, WEIGHTED_COMP_PCT, COMP_WEIGHTED_AVERAGE;
        
        CREATE TABLE last_step2 AS 
        SELECT areasymbol, musym, muname,
        kitchensink.mukey, last_step.COKEY,
        CAST (SUM (COMP_WEIGHTED_AVERAGE1) over(partition by kitchensink.mukey) as decimal(5,2))AS """ + col + """
        FROM kitchensink  
        LEFT OUTER JOIN last_step ON kitchensink.mukey=last_step.mukey
        GROUP BY kitchensink.areasymbol, kitchensink.musym, kitchensink.muname, kitchensink.mukey, COMP_WEIGHTED_AVERAGE1, last_step.COKEY
        ORDER BY kitchensink.areasymbol, kitchensink.musym, kitchensink.muname, kitchensink.mukey;
        
        
        CREATE TABLE """ + tblname + """ AS
        SELECT last_step2.areasymbol, last_step2.musym, last_step2.muname,
        last_step2.mukey, CAST(ROUND (last_step2.""" + col + """, 2) AS REAL) AS """ + col + """
        FROM last_step2
        LEFT OUTER JOIN last_step ON last_step.mukey=last_step2.mukey
        GROUP BY last_step2.areasymbol, last_step2.musym, last_step2.muname, last_step2.mukey, last_step2.""" + col + """
        ORDER BY last_step2.areasymbol, last_step2.musym, last_step2.muname, last_step2.mukey, last_step2.""" + col + """;
        
        DROP TABLE IF EXISTS kitchensink;
        DROP TABLE IF EXISTS comp_temp;
        DROP TABLE IF EXISTS comp_temp2;
        DROP TABLE IF EXISTS comp_temp3;
        DROP TABLE IF EXISTS last_step;
        DROP TABLE IF EXISTS last_step2;
        DROP TABLE IF EXISTS temp_main;"""
        
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_wtdavg = qry_wtdavg + gcontents

        else:
            pass            
        
        return test, qry_wtdavg
    
    
    def dcpn(self, col, tDep, bDep, dbtype):
        
        tblname = 'SSURGOOnDemand_dom_comp_' + col + '_' + tDep + '_' + bDep
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;"""
        
        qry_dcpn = """--dominant component numeric
        DROP TABLE IF EXISTS kitchensink;
        DROP TABLE IF EXISTS comp_temp;
        DROP TABLE IF EXISTS comp_temp2;
        DROP TABLE IF EXISTS comp_temp3;
        DROP TABLE IF EXISTS last_step;
        DROP TABLE IF EXISTS last_step2;
        DROP TABLE IF EXISTS temp_main;
        
        
        CREATE TABLE kitchensink AS
        SELECT areasymbol, musym, muname, mukey
        FROM legend  AS lks
        INNER JOIN  mapunit AS muks ON muks.lkey = lks.lkey;  
        
        CREATE TABLE comp_temp AS		
        SELECT mu1.mukey, cokey, comppct_r,
        SUM (comppct_r) over(partition by mu1.mukey ) AS SUM_COMP_PCT
        FROM kitchensink AS mu1
        INNER JOIN  component AS c1 ON c1.mukey = mu1.mukey AND majcompflag = 'Yes' AND c1.cokey =
        (SELECT c2.cokey FROM component AS c2
        INNER JOIN mapunit AS mm1 ON c2.mukey=mm1.mukey AND c2.mukey=mu1.mukey ORDER BY CASE WHEN compkind = 'Miscellaneous area' THEN 2 ELSE 1 END ASC, c2.comppct_r DESC, c2.cokey LIMIT 1) 
        -- If the first component is Misc. Then go to the next component
        --Subquery to get dominant component
        ;	
        
        CREATE TABLE comp_temp3 AS
        SELECT cokey, SUM_COMP_PCT, CASE WHEN comppct_r = SUM_COMP_PCT THEN 1
        ELSE CAST (CAST (comppct_r AS  REAL) / CAST (SUM_COMP_PCT AS REAL) AS REAL) END AS WEIGHTED_COMP_PCT
        FROM comp_temp;	
        
        CREATE TABLE temp_main AS		
        SELECT
        areasymbol, musym, muname, mu.mukey/1  AS MUKEY, c.cokey AS COKEY, ch.chkey/1 AS CHKEY, compname, hzname, hzdept_r, hzdepb_r, CASE WHEN hzdept_r <""" + tDep + """  THEN 0 ELSE hzdept_r END AS hzdept_r_ADJ,
        CASE WHEN hzdepb_r > """ + bDep + """  THEN """ + bDep + """ ELSE hzdepb_r END AS hzdepb_r_ADJ,
        CAST (CASE WHEN hzdepb_r > """ + bDep + """  THEN """ + bDep + """ ELSE hzdepb_r END - CASE WHEN hzdept_r <""" + tDep + """ THEN 0 ELSE hzdept_r END AS decimal (5,2)) AS thickness,
        comppct_r,
        CAST (SUM (CASE WHEN hzdepb_r > """ + bDep + """  THEN """ + bDep + """ ELSE hzdepb_r END - CASE WHEN hzdept_r <""" + tDep + """ THEN 0 ELSE hzdept_r END) over(partition by c.cokey) AS decimal (5,2)) AS sum_thickness,
        CAST (IFNULL (""" + col + """, 0) AS decimal (5,2))AS """ + col + """
        
        FROM kitchensink  AS mu
        INNER JOIN  component AS c ON c.mukey = mu.mukey
        INNER JOIN chorizon AS ch ON ch.cokey=c.cokey AND hzname NOT LIKE '%O%'AND hzname NOT LIKE '%r%'
        AND hzdepb_r >""" + tDep + """ AND hzdept_r <""" + bDep + """
        INNER JOIN chtexturegrp AS cht ON ch.chkey=cht.chkey  WHERE cht.rvindicator = 'Yes' AND  ch.hzdept_r IS NOT NULL
        AND texture NOT LIKE '%PM%' and texture NOT LIKE '%DOM' and texture NOT LIKE '%MPT%' and texture NOT LIKE '%MUCK' and texture NOT LIKE '%PEAT%' and texture NOT LIKE '%br%' and texture NOT LIKE '%wb%'
        ORDER BY areasymbol, musym, muname, mu.mukey, comppct_r DESC, cokey,  hzdept_r, hzdepb_r	;	
        
        CREATE TABLE comp_temp2 AS 
        SELECT temp_main.areasymbol, temp_main.musym, temp_main.muname, temp_main.MUKEY,
        temp_main.COKEY, temp_main.CHKEY, temp_main.compname, hzname, hzdept_r, hzdepb_r, hzdept_r_ADJ, hzdepb_r_ADJ, thickness, sum_thickness, """ + col + """, comppct_r, SUM_COMP_PCT, WEIGHTED_COMP_PCT ,
        SUM((CAST (thickness  AS REAL )/CAST (sum_thickness  AS REAL ) ) * """ + col + """ )over(partition by temp_main.COKEY)AS COMP_WEIGHTED_AVERAGE
        FROM temp_main
        INNER JOIN comp_temp3 ON comp_temp3.cokey=temp_main.cokey
        ORDER BY temp_main.areasymbol, temp_main.musym, temp_main.muname, temp_main.MUKEY, comppct_r DESC,  temp_main.COKEY,  hzdept_r, hzdepb_r;
        
        CREATE TABLE last_step AS 
        SELECT comp_temp2.MUKEY,comp_temp2.COKEY, WEIGHTED_COMP_PCT * COMP_WEIGHTED_AVERAGE AS COMP_WEIGHTED_AVERAGE1
        FROM comp_temp2
        GROUP BY  comp_temp2.MUKEY,comp_temp2.COKEY, WEIGHTED_COMP_PCT, COMP_WEIGHTED_AVERAGE;
        
        CREATE TABLE last_step2 AS 
        SELECT areasymbol, musym, muname,
        kitchensink.mukey, last_step.COKEY,
        CAST (SUM (COMP_WEIGHTED_AVERAGE1) over(partition by kitchensink.mukey) as decimal(5,2))AS """ + col + """
        FROM kitchensink  
        LEFT OUTER JOIN last_step ON kitchensink.mukey=last_step.mukey
        GROUP BY kitchensink.areasymbol, kitchensink.musym, kitchensink.muname, kitchensink.mukey, COMP_WEIGHTED_AVERAGE1, last_step.COKEY
        ORDER BY kitchensink.areasymbol, kitchensink.musym, kitchensink.muname, kitchensink.mukey;
        
        
        CREATE TABLE """ + tblname + """ AS SELECT last_step2.areasymbol, last_step2.musym, last_step2.muname,
        last_step2.mukey, CAST(ROUND (last_step2.""" + col + """, 2) AS REAL) AS """ + col + """
        FROM last_step2
        LEFT OUTER JOIN last_step ON last_step.mukey=last_step2.mukey
        GROUP BY last_step2.areasymbol, last_step2.musym, last_step2.muname, last_step2.mukey, last_step2.""" + col + """
        ORDER BY last_step2.areasymbol, last_step2.musym, last_step2.muname, last_step2.mukey, last_step2.""" + col + """;
        
        DROP TABLE IF EXISTS kitchensink;
        DROP TABLE IF EXISTS comp_temp;
        DROP TABLE IF EXISTS comp_temp2;
        DROP TABLE IF EXISTS comp_temp3;
        DROP TABLE IF EXISTS last_step;
        DROP TABLE IF EXISTS last_step2;
        DROP TABLE IF EXISTS temp_main;"""
        
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_dcpn = qry_dcpn + gcontents

        else:
            pass            
        
        # print(self.qry_dcpn)
        return test, qry_dcpn
        
    
    def exeq(self, qry, kind=None):
        
        import sqlite3
        from contextlib import closing
        
        try:
            
            with closing(sqlite3.connect(self.db)) as conn:
                with closing(conn.cursor()) as cur:
                    cur = conn.cursor()
                    if kind == 'select':
                        cur.execute(qry)
                        result = cur.fetchone()[0]
                        return result
                    elif kind is None:
                        cur.executescript(qry)
                    cur.close()
        
        except Exception as e:
            print(qry)
            print(e)
            self.invalid(message=e)
                        
    
    def proplu(self, prop):

        propD = {'0.1 bar H2O - Rep Value' : 'wtenthbar_r', '0.33 bar H2O - Rep Value' : 'wthirdbar_r', '15 bar H2O - Rep Value' : 'wfifteenbar_r', 'Available Water Capacity - Rep Value' : 'awc_r', 'Bray 1 Phosphate - Rep Value' : 'pbray1_r', 'Bulk Density 0.1 bar H2O - Rep Value' : 'dbtenthbar_r', 'Bulk Density 0.33 bar H2O - Rep Value' : 'dbthirdbar_r', 'Bulk Density 15 bar H2O - Rep Value' : 'dbfifteenbar_r', 'Bulk Density oven dry - Rep Value' : 'dbovendry_r', 'CaCO3 Clay - Rep Value' : 'claysizedcarb_r', 'Calcium Carbonate - Rep Value' : 'caco3_r', 'Cation Exchange Capcity - Rep Value' : 'cec7_r', 'Coarse Sand - Rep Value' : 'sandco_r', 'Coarse Silt - Rep Value' : 'siltco_r', 'Corrosion of Steel' : 'corsteel', 'Corrosion of Concrete' : 'corcon', 'Drainage Class' : 'drainagecl', 'Effective Cation Exchange Capcity - Rep Value' : 'ecec_r', 'Electrial Conductivity 1:5 by volume - Rep Value' : 'ec15_r', 'Electrical Conductivity - Rep Value' : 'ec_r', 'Exchangeable Sodium Percentage - Rep Value' : 'esp_r', 'Extract Aluminum - Rep Value' : 'extral_r', 'Extractable Acidity - Rep Value' : 'extracid_r', 'Fine Sand - Rep Value' : 'sandfine_r', 'Fine Silt - Rep Value' : 'siltfine_r', 'Free Iron - Rep Value' : 'freeiron_r', 'Gypsum - Rep Value' : 'gypsum_r', 'Hydrologic Group' : 'hydgrp', 'Kf' : 'kffact', 'Kw ' : 'kwfact', 'LEP - Rep Value' : 'lep_r', 'Liquid Limit - Rep Value' : 'll_r', 'Medium Sand - Rep Value' : 'sandmed_r', 'Organic Matter - Rep Value' : 'om_r', 'Oxalate Aluminum - Rep Value' : 'aloxalate_r', 'Oxalate Iron - Rep Value' : 'feoxalate_r', 'Oxalate Phosphate - Rep Value' : 'poxalate_r', 'Plasticity Index - Rep Value' : 'pi_r', 'Rock Fragments 3 - 10 cm - Rep Value' : 'frag3to10_r', 'Rock Fragments > 10 cm - Rep Value' : 'fraggt10_r', 'Satiated H2O - Rep Value' : 'wsatiated_r', 'Saturated Hydraulic Conductivity - Rep Value' : 'ksat_r', 'Sodium Adsorption Ratio - Rep Value' : 'sar_r', 'Sum of Bases - Rep Value' : 'sumbases_r', 'Taxonomic Class Name' : 'taxclname', 'Taxonomic Order' : 'taxorder', 'Taxonomic Particle Size' : 'taxpartsize', 'Taxonomic Suborder' : 'taxsuborder', 'Taxonomic Temperature Regime' : 'taxtempregime', 'Total Clay - Rep Value' : 'claytotal_r', 'Total Phosphate - Rep Value' : 'ptotal_r', 'Total Rock Fragment Volume - Rep Value' : 'fragvoltot_r', 'Total Sand - Rep Value' : 'sandtotal_r', 'Total Silt - Rep Value' : 'silttotal_r', 'Very Coarse Sand - Rep Value' : 'sandvc_r', 'Very Fine Sand - Rep Value' : 'sandvf_r', 'Water Soluble Phosphate - Rep Value' : 'ph2osoluble_r', 'Wind Erodibility Group' : 'weg', 'Wind Erodibility Index' : 'wei', 'no. 10 sieve - Rep Value' : 'sieveno10_r', 'no. 200 sieve - Rep Value' : 'sieveno200_r', 'no. 4 sieve - Rep Value' : 'sieveno4_r', 'no. 40 sieve - Rep Value' : 'sieveno40_r', 'pH .01M CaCl2 - Rep Value' : 'ph01mcacl2_r', 'pH 1:1 water - Rep Value' : 'ph1to1h2o_r', 'pH Oxidized - Rep Value' : 'phoxidized_r', 't Factor' : 'tfact'}
        propV = propD.get(prop)
        
        return propV
    
    
    def close_windows(self):
        self.master.destroy()
    
        
class Interpretations:
   
    def __init__(self, master):
        
        self.master = master
        self.master.title('Interpretations - SSURGO On-Demand')
        self.frame = tkinter.Frame(self.master)
        
        base = sys.argv[0]
        bDir = os.path.dirname(base)
        ico = os.path.join(bDir, 'ncss.ico')
        png = os.path.join(bDir, 'ncss.png')
        
        try:
        	self.master.iconbitmap(ico)
        
        except:
            
            if os.path.exists(png):
            
                img = tkinter.Image("photo", file=png)
                self.master.tk.call('wm','iconphoto',self.master._w,img)
        
            else:
                pass

        
        f = ("DejaVuSans", 10, "bold")
        
        # === select tempalte dbframe
        self.openFrame = tkinter.LabelFrame(self.frame, text='Select Template Database', font=f)
        self.openFrame.grid(sticky = 'w', row=0, column=0, padx = 15, pady= 10)
        self.OpenButton = tkinter.Button(self.openFrame, text="Open", width=10, command=self.openDB)
        self.OpenButton.grid(row=0, padx=10, pady=10)
        
        self.openLbl=tkinter.Label(self.openFrame, text=None, padx=0, pady=0)
        self.openLbl.grid(sticky = 'w', row=0, column=1)
        
        # === aggregation method frame
        self.methods = ['Dominant Component', 'Dominant Condition', 'Weighted Average']
        
        self.aggFrame = tkinter.LabelFrame(self.frame, text='Select Aggregation Method', font=f)
        self.aggFrame.grid(sticky = 'w', row=1, column=0, padx = 15, pady= 10)
        
        self.aggChoices = tkinter.StringVar()
        
        self.aggChoices.trace('r', self.callback)
        
        self.aggChoices.set(self.methods[0])
        self.aggMethod = tkinter.OptionMenu(self.aggFrame, self.aggChoices, *self.methods, command=self.callback)
        self.aggMethod.grid(row=0, column=0, padx=10, pady=10) 
        # self.aggSubmit = tkinter.Button(self.aggFrame, text = 'Submit', width = 10)#,  command=self.intGen)
        # self.aggSubmit.grid(row=0, column=1, padx=10, pady=10)
        
        # === soil interps frame         
        self.interpFrame = tkinter.LabelFrame(self.frame, text='Select Soil Interpretations', font=f)
        self.interpFrame.grid(sticky = 'w', row=2, column=0, padx = 15, pady= 10)
        
        self.scrollbar = tkinter.Scrollbar(self.interpFrame)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        self.interps = tkinter.Listbox(self.interpFrame, selectmode='multiple', width=50)
        self.interps.grid(row=0, padx=10, pady=10)
        self.interps.configure(exportselection=False)
        
        self.interps.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.interps.yview)
        # self.interps.configure(scrollregion=self.interps.bbox("active"))
        
        
        self.runFrame = tkinter.LabelFrame(self.frame, text='Execute', font=f)
        self.runFrame.grid(row=3, column=0, padx = 15, pady= 10)
        
        self.execButton = tkinter.Button(self.runFrame, text = 'Run', width = 25, command = self.run)
        self.execButton.grid(row=0, column=0, padx=10, pady=10)
        self.execButton["activebackground"] = "#d8e1d9"
        
        self.quitButton = tkinter.Button(self.runFrame, text = 'Cancel', width = 25, command = self.close_windows)
        self.quitButton.grid(row=0, column=1, padx=10, pady=10)
        
    
        self.frame.pack()
        
        # print(self.db)
        
    
    def openDB(self):
        
        import tkinter.filedialog
        self.db = tkinter.filedialog.askopenfilename(parent=self.frame,  initialdir="", title="Select SSURGO Template Database", filetypes=(("SQLite", " *.gpkg"), ("SQLite", "*.sqlite"), ("All Files", "*")))
        typind = self.db.rfind(".")
        self.dtype = self.db[typind:]
        
        if self.db:
            q = """SELECT COUNT(*) FROM sacatalog;"""
            sacount = self.exeq(q, kind='select')
            # print(self.sacount)
        
        if sacount[0][0] < 1:
            message = 'Database does not appear to be a populated SSURGO database'
            self.interps.delete(0, 'end')
            self.invalid(message=message)
            
        else:
            q = """SELECT DISTINCT interpname
                from sainterp;"""
            interList = self.exeq(q, kind='select')
            
            if len(interList) < 1:
                self.interps.delete(0, 'end')
                message = 'Unable to retrieve valid list of available interpretations'
                self.invalid(message=message)
                
            else:
                self.openLbl=tkinter.Label(self.openFrame, text=self.db, bg = 'white',  padx=5, pady=5)
                self.openLbl.grid(sticky = 'w', row=0, column=1)
                
                
                for i,item in enumerate(interList):
                    self.interps.insert(i, item[0])
                    
        
    def callback(self, *args):
        
        choice = self.aggChoices.get()
        return choice
    
    
    def exeq(self, qry, kind=None):
        
        import sqlite3
        from contextlib import closing
        
        try:
            
            with closing(sqlite3.connect(self.db)) as conn:
                with closing(conn.cursor()) as cur:
                    cur = conn.cursor()
                    if kind == 'select':
                        cur.execute(qry)
                        result = cur.fetchall()
                        # print(result)
                        return result
                    elif kind is None:
                        cur.executescript(qry)
                    cur.close()
        
        except Exception as e:
            print(e)
            self.invalid(message=e)
        
    
    def idomcond(self, iname, dbtype):
        
        itable = re.sub('[^0-9a-zA-Z]+', '_', iname)
        tblname = 'SSURGOOnDemand_dom_cond_' + itable 
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;
        DROP TABLE IF EXISTS SSURGOOnDemand_domcond_temp;
        DROP TABLE IF EXISTS SSURGOOnDemand_domcond_temp2;"""
        
        qry_domcond = """--dominant condition

        CREATE TABLE SSURGOOnDemand_domcond_temp AS
        SELECT  cokey
              ,mrulekey 
              ,mrulename
        	  ,rulename
              ,ruledepth
              ,interphr 
              ,interphrc
        	  ,cointerpkey
        
        FROM[cointerp] WHERE mrulename = '""" + iname + """' ;
        
        
         CREATE TABLE SSURGOOnDemand_domcond_temp2 AS SELECT areasymbol, musym, muname, CAST(mu.mukey/1 AS INT)  AS mukey, 
         (SELECT ROUND (AVG(interphr) over(partition by interphrc),2)
         FROM mapunit
         INNER JOIN component ON component.mukey=mapunit.mukey AND majcompflag = 'Yes'
         INNER JOIN SSURGOOnDemand_domcond_temp ON component.cokey = SSURGOOnDemand_domcond_temp.cokey AND mapunit.mukey = mu.mukey AND ruledepth = 0 AND mrulename LIKE '""" + iname + """' GROUP BY interphrc,
         interphr ORDER BY SUM (comppct_r) DESC LIMIT 1) AS rating,
         (SELECT interphrc
         FROM mapunit
         INNER JOIN component ON component.mukey=mapunit.mukey AND majcompflag = 'Yes'
         INNER JOIN SSURGOOnDemand_domcond_temp ON component.cokey = SSURGOOnDemand_domcond_temp.cokey AND mapunit.mukey = mu.mukey AND ruledepth = 0 AND mrulename LIKE '""" + iname + """'
         GROUP BY interphrc, comppct_r ORDER BY SUM(comppct_r) over(partition by interphrc) DESC LIMIT 1) as class,
         
          (SELECT GROUP_CONCAT( DISTINCT interphrc)
        FROM mapunit
        INNER JOIN component ON component.mukey=mapunit.mukey AND compkind != 'miscellaneous area' 
        INNER JOIN SSURGOOnDemand_domcond_temp ON component.cokey = SSURGOOnDemand_domcond_temp.cokey AND mapunit.mukey = mu.mukey AND majcompflag = 'Yes'
        AND ruledepth != 0 AND interphrc NOT LIKE 'Not%' AND mrulename LIKE '""" + iname + """' GROUP BY interphrc
        ORDER BY interphr DESC, interphrc
         )as reason
          
         FROM legend  AS l
         INNER JOIN  mapunit AS mu ON mu.lkey = l.lkey 
         ORDER BY areasymbol, musym, muname, mu.mukey;
         
         CREATE TABLE """ + tblname + """ AS SELECT CAST(areasymbol AS text) AS areasymbol, CAST(musym AS test) AS musym, CAST(muname AS text) AS muname, 
         CAST(mukey As INT) AS mukey, CAST(rating AS REAL) AS rating, CAST(class AS text) AS class, CAST(reason AS text) AS reason
         FROM SSURGOOnDemand_domcond_temp2;
         
         DROP TABLE IF EXISTS SSURGOOnDemand_domcond_temp;
         DROP TABLE IF EXISTS SSURGOOnDemand_domcond_temp2;"""
         
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_domcond = qry_domcond + gcontents
        
        # print(qry_domcond)
        return test, qry_domcond
    
    
    def idomcomp(self, iname, dbtype):
        
        itable = re.sub('[^0-9a-zA-Z]+', '_', iname)
        tblname = 'SSURGOOnDemand_dom_comp_' + itable 
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;
        DROP TABLE IF EXISTS cointerp_idomcomp;
        DROP TABLE IF EXISTS cointerp_idomcomp2;"""
        
        qry_domcomp = """--dominant component

        CREATE TABLE cointerp_idomcomp AS
        SELECT  cokey
        ,mrulekey 
        ,mrulename
    	,rulename
        ,ruledepth
        ,interphr 
        ,interphrc
    	,cointerpkey

        FROM[cointerp] WHERE mrulename = '""" + iname + """';
        
        
        CREATE TABLE cointerp_idomcomp2 AS SELECT areasymbol, musym, muname, mu.mukey/1  AS mukey, 
        (SELECT ROUND (AVG(interphr) over(partition by interphrc),2)
        FROM mapunit
        INNER JOIN component ON component.mukey=mapunit.mukey
        INNER JOIN cointerp_idomcomp ON component.cokey = cointerp_idomcomp.cokey AND mapunit.mukey = mu.mukey AND ruledepth = 0 AND mrulename LIKE '""" + iname + """' GROUP BY interphrc, interphr
        ORDER BY SUM (comppct_r) DESC LIMIT 1)as rating,
        (SELECT interphrc
        FROM mapunit
        INNER JOIN component ON component.mukey=mapunit.mukey
        INNER JOIN cointerp_idomcomp ON component.cokey = cointerp_idomcomp.cokey AND mapunit.mukey = mu.mukey AND ruledepth = 0 AND mrulename LIKE '""" + iname + """'
        GROUP BY interphrc, comppct_r ORDER BY SUM(comppct_r) over(partition by interphrc) DESC LIMIT 1) as class,
         
        (SELECT GROUP_CONCAT( DISTINCT interphrc)
        FROM mapunit
        INNER JOIN component ON component.mukey=mapunit.mukey AND compkind != 'miscellaneous area' 
        INNER JOIN cointerp_idomcomp ON component.cokey = cointerp_idomcomp.cokey AND mapunit.mukey = mu.mukey 
        AND ruledepth != 0 AND interphrc NOT LIKE 'Not%' AND mrulename LIKE '""" + iname + """' 
        ORDER BY interphr DESC, interphrc) as reason
          
        FROM legend  AS l
        INNER JOIN  mapunit AS mu ON mu.lkey = l.lkey 
        INNER JOIN component AS c1 ON c1.mukey=mu.mukey 
        AND c1.cokey =
        (SELECT c2.cokey FROM component AS c2
        INNER JOIN mapunit AS mm1 ON c2.mukey=mm1.mukey AND c2.mukey=mu.mukey ORDER BY c2.comppct_r DESC, c2.cokey LIMIT 1)
        ORDER BY areasymbol, musym, muname, mu.mukey;
        
       CREATE TABLE """ + tblname + """ AS SELECT CAST(areasymbol AS text) AS areasymbol, CAST(musym AS test) AS musym, CAST(muname AS text) AS muname, 
       CAST(mukey As INT) AS mukey, CAST(rating AS REAL) AS rating, CAST(class AS text) AS class, CAST(reason AS text) AS reason
        FROM cointerp_idomcomp2;
         
        DROP TABLE IF EXISTS cointerp_idomcomp;
        DROP TABLE IF EXISTS cointerp_idomcomp2;"""
         
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_domcomp = qry_domcomp + gcontents
        
        # print(qry_domcomp)
        return test, qry_domcomp
    
    
    def iwtdavg(self, iname, dbtype):
        
        itable = re.sub('[^0-9a-zA-Z]+', '_', iname)
        tblname = 'SSURGOOnDemand_wtd_avg_' + itable 
        
        test = """DROP TABLE IF EXISTS """ + tblname + """;
        DROP TABLE IF EXISTS cointerp_lite_temp;"""
        
        qry_wtdavg = """--weighted average
        DROP TABLE IF EXISTS temp_main;
        DROP TABLE IF EXISTS cointerp_lite_temp;
        
        CREATE TABLE cointerp_lite_temp AS
        SELECT  cokey
              ,mrulekey 
              ,mrulename
        	  ,rulename
              ,ruledepth
              ,interphr 
              ,interphrc
        	  ,cointerpkey
        FROM[cointerp] WHERE mrulename = '""" + iname + """';
        
        
        	CREATE TABLE temp_main AS SELECT areasymbol, musym, muname, mu.mukey/1  AS mukey,
        
        		ROUND ((SELECT SUM (interphr * comppct_r)
        		FROM mapunit
        		INNER JOIN component ON component.mukey=mapunit.mukey AND majcompflag = 'Yes'
        		INNER JOIN cointerp_lite_temp ON component.cokey = cointerp_lite_temp.cokey AND mapunit.mukey = mu.mukey AND ruledepth = 0 AND mrulename LIKE '""" + iname + """'
        		GROUP BY mapunit.mukey),2) as rating,
        		ROUND ((SELECT SUM (comppct_r)
        		FROM mapunit
        		INNER JOIN component ON component.mukey=mapunit.mukey AND majcompflag = 'Yes'
        		INNER JOIN cointerp_lite_temp ON component.cokey = cointerp_lite_temp.cokey AND mapunit.mukey = mu.mukey AND ruledepth = 0 AND mrulename LIKE '""" + iname + """'
        		AND (interphr) IS NOT NULL GROUP BY mapunit.mukey),2) as sum_com, 
        		  (SELECT GROUP_CONCAT( DISTINCT interphrc)
        FROM mapunit
        INNER JOIN component ON component.mukey=mapunit.mukey AND compkind != 'miscellaneous area' AND majcompflag = 'Yes'
        INNER JOIN cointerp_lite_temp ON component.cokey = cointerp_lite_temp.cokey AND mapunit.mukey = c.mukey 
        AND ruledepth != 0 AND interphrc NOT LIKE 'Not%' AND mrulename LIKE '""" + iname + """' 
        ORDER BY interphr DESC, interphrc
         )as reason
               
                    
                   
                    FROM legend  AS l
                    INNER JOIN  mapunit AS mu ON mu.lkey = l.lkey
                    INNER JOIN  component AS c ON c.mukey = mu.mukey AND majcompflag = 'Yes'
                    GROUP BY areasymbol, musym, muname, mu.mukey;
                    
        CREATE TABLE """ + tblname + """ AS SELECT CAST(areasymbol AS text) AS areasymbol, CAST(musym AS text) AS musym, 
        CAST(muname AS text) AS muname, CAST(mukey AS INT) AS mukey, CAST(rating/sum_com AS REAL) AS rating, CAST(reason AS text) AS reason
        FROM temp_main;
        
        DROP TABLE IF EXISTS temp_main;
        DROP TABLE IF EXISTS cointerp_lite_temp;""" 
       
        if dbtype == '.gpkg':
            
            gtest = """
            DELETE FROM gpkg_contents
            WHERE table_name = '""" + tblname + """';"""
            
            test = test + gtest
            
            gcontents = """INSERT INTO gpkg_contents 
            (table_name, data_type, identifier, description, min_x, min_y, max_x, max_y, srs_id)
            VALUES ('""" + tblname + """', 'attributes','""" + tblname + """', '', -180.0, -90.0, 180.0, 90, 4326);"""
            
            qry_wtdavg = qry_wtdavg + gcontents
        
        # print(test)
        # print(qry_wtdavg)
       
        return test, qry_wtdavg
       
          
    def run(self):
        
        message = ''
        
        method = self.aggChoices.get()
        intInd = self.interps.curselection()
        intRun = "*".join([self.interps.get(i) for i in intInd])
        
        if self.openLbl.cget("text") == '':
            message = 'Invalid database'
            self.invalid(message)
        
        if message == '':
            
            if intRun == '':
                message = 'Select at least 1 soil interpretation'
                self.invalid(message)
            
            if message == '':
                
                itrint = intRun.split('*')
                
                if method == 'Dominant Condition':
                    for i in itrint:
                    
                        tQry, pQry = self.idomcond(i, self.dtype)
                        self.exeq(tQry, kind=None)
                        self.exeq(pQry, kind=None)
                        
                elif method == 'Dominant Component':
                    for i in itrint:
                    
                        tQry, pQry = self.idomcomp(i, self.dtype)
                        self.exeq(tQry, kind=None)
                        self.exeq(pQry, kind=None)
                        
                elif method == 'Weighted Average':
                    for i in itrint:
                        
                        tQry, pQry = self.iwtdavg(i, self.dtype)
                        self.exeq(tQry, kind=None)
                        self.exeq(pQry, kind=None)
    
    
    def invalid(self, message):
        from tkinter import messagebox
        self.mbox = tkinter.messagebox.showerror('Error',  message=message, parent=self.frame)
            
    
    def close_windows(self):
        self.master.destroy()

def main(): 
    root = tkinter.Tk()
    app = Splash(root)
    base = sys.argv[0]
    bDir = os.path.dirname(base)
    ico = os.path.join(bDir, 'ncss.ico')
    png = os.path.join(bDir, 'ncss.png')
    
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(ico)

    except:
        
        if os.path.exists(png):
        
            img = tkinter.Image("photo", file=png)
            root.tk.call('wm','iconphoto',root._w,img)
        
        else:
            
            pass
    
    root.mainloop()
    

if __name__ == '__main__':
    main()