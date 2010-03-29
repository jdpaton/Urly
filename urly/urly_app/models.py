from django.db import models
from datetime import datetime

class Urly(models.Model):


      
  key = models.CharField(max_length=128, unique=True)
  created = models.DateTimeField(auto_now = True)
  url = models.URLField(verify_exists = True, unique=True)
  hits = models.IntegerField()
  last_hit = models.DateTimeField()
  request_ip = models.IPAddressField()
  expired = models.BooleanField()
  private = models.BooleanField()
  
  class Meta:
    ordering = ["-created"]
    verbose_name_plural = "Urlies"

  def get_new_key(self):
    
    alpha_symbols = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
    num_symbols = [ str(i) for i in range(0, 10)]
    symbols = alpha_symbols + num_symbols
    
    if Urly.objects.count() == 0:
      return symbols[0]
    
    expired_exists = Urly.objects.filter(expired=True).count()
    
    if expired_exists:
      u = Urly.objects.filter(expired=True)[0]
      
      u.delete()
      
      return u.key
      
    else:
      u = Urly.objects.filter(expired=False)
      
      def new_key(old_key):
        
        
        if old_key[-1] == symbols[-1]:
          
          c = 0
          #print 'old: ' + old_key
          for i in reversed(old_key):
            
            
            for j in old_key[0:len(old_key)]:
              
              if j == symbols[-1]:
                c = c + 1
                
          
          if not c or len(old_key) == 2:
            inc = old_key[-2]
            old_key = old_key[:-2]
            old_key = old_key + symbols[symbols.index(inc)+1] + symbols[0]
            
          else:
            if len(old_key) == c / len(old_key):
              old_key = symbols[0] * (len(old_key) + 1)
              
            else:
              v = c / len(old_key)
              inc = old_key[-v]
              old_key = old_key[:-v] + symbols[0] + (symbols[0] * (v-1))
            
          
        else:
          
          old_key = old_key[0:-1] + symbols[symbols.index(old_key[-1])+1 ]
        
        #print 'new: ' + old_key
        return old_key
        
      for y in u:
        
        
        return new_key(y.key)
