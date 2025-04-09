import { ApplianceType } from "@/lib/types"
import { Separator } from "@/components/ui/separator"

export function ApplianceInfo({ 
  appliance,
}: {
  appliance: ApplianceType
}) {
  return (
    <div className="px-4 py-3 h-auto">
      <div className="text-lg font-bold mb-2">기능</div>
      <Separator className="my-2 bg-gray-300" />
      <div className="space-y-0.5 grid grid-cols-2 gap-x-8 gap-y-2">
        {appliance.modelSpecs.map((spec, index) => (
          <div key={index} className="flex justify-between text-sm h-5">
            <span className="font-medium">{spec.specName}</span>
              <span className="text-muted-foreground font-light">{spec.specValue}</span>
            </div>
          ))}
      </div>
    </div>
  )
}
