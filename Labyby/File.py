class File:
    def __init__(self): self.contenu=[]
    def est_vide(self): return self.contenu==[]
    def enfiler(self,x): self.contenu.append(x)
    def taille(self): return len(self.contenu)
    def present(self,x): return x in self.contenu
    def defiler(self):
        assert not self.est_vide(),"File vide !"
        return self.contenu.pop(0)   #ou del self.file[-1]
    def sommet(self):
        assert not self.est_vide(),"File vide !"
        return self.contenu[0]
    