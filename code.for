program test; {programa exemplo}
var
  ii : integer;
  rr : real;
  bb: boolean;

procedure outer(ii: real);
  var
    r2: real;
    i2: integer;

  procedure inner;
    begin
    doing := stuff {vai dar errado}
    end;
  
  begin
    r2 := ii + 5 ; {vai dar certo}
    i2 := r2 + i2; {vai dar errado}
    r2 := i2 + 45.3 + 129 + r2
  end
  ;

begin
end
.