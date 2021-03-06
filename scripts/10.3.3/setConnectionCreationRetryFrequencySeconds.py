import getopt

configFileProd='prd.config'
keyFileProd='prd.key'
configFileAcc='acc.config'
keyFileAcc='acc.key'
configFileSim='sim.config'
keyFileSim='sim.key'

def connecttoadmin(configFileProd,keyFileProd,adminurl):
        print '=============================================='
        connect(userConfigFile=configFileProd,userKeyFile=keyFileProd, url=adminurl)
        print '=============================================='

def setConnectionCreationRetryFrequencySeconds():
        dsMBeans = cmo.getJDBCSystemResources()
        for ds in dsMBeans:
                #check if jdbcresource is a multipool or a datasource
                if not ds.getJDBCResource().getJDBCDataSourceParams().getDataSourceList():
                        print '=============================================='
                        print 'Name : \t\t\t '+ ds.getName()
                        print 'ConnectionCreationRetryFrequency before : \t ' + str(ds.getJDBCResource().getJDBCConnectionPoolParams().getConnectionCreationRetryFrequencySeconds())
                        try:
                                ds.getJDBCResource().getJDBCConnectionPoolParams().setConnectionCreationRetryFrequencySeconds(3)
                        except:
                                dumpStack()
                        print 'ConnectionCreationRetryFrequency after  : \t ' + str(ds.getJDBCResource().getJDBCConnectionPoolParams().getConnectionCreationRetryFrequencySeconds())
                        print '=============================================='

def validateAndShowChanges():
        try:
                validate()
        except WLSTException:
                print "Couldn't validate"
                dumpStack()
                sys.exc_info()
                sys.exit(2)
        print '============== changes ======================'
        showChanges()
        print '=============================================='
        try:
                save()
        except WLSTException:
                print "Couldn't save"
                dumpStack()
                sys.exc_info()
                sys.exit(2)
        try:
                activate()
        except WLSTException:
                print "Couldn't activate"
                dumpStack()
                sys.exc_info()
                sys.exit(2)

def usage():
        print sys.argv[0]+" -e {acc|prd|sim} t3://adminurl:port/"
try     :
        opts,args = getopt.getopt(sys.argv[1:],"e:")
except getopt.GetoptError       :
        #print help information and exit        :
        usage()
        sys.exit(2)
for o, a in opts :
        if o == "-e" :
                env = a
if len(args) != 1:
        usage()
        sys.exit(2)
try:
        if env =='acc':
                print 'connect to acc domain'
                connecttoadmin(configFileAcc,keyFileAcc,args[0])
        elif env == 'prd':
                print 'connect to prd domain'
                connecttoadmin(configFileProd,keyFileProd,args[0])
        elif env == 'sim':
                print 'connect to sim domain'
                connecttoadmin(configFileSim,keyFileSim,args[0])
        else:
                print 'not supported env used : ' + env
                usage()
        #redirect WLST native output to /dev/null
        #redirect("/dev/null",'false')
        edit()
        startEdit()
        setConnectionCreationRetryFrequencySeconds()
        validateAndShowChanges()
        disconnect()
except:
        dumpStack()
        sys.exc_info()
        sys.exit(2)
