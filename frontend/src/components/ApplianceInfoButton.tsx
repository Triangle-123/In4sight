"use client"

import { ChevronDown, ChevronRight } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Separator } from "@/components/ui/separator"
import type { ApplianceType } from "@/lib/types"

interface SidebarApplianceInfoProps {
  appliance: ApplianceType
  isActive?: boolean
  isOpen?: boolean
  onOpenChange?: (open: boolean) => void
  onClick?: () => void
}

export function SidebarApplianceInfo({ 
  appliance, 
  isActive, 
  isOpen = false, 
  onOpenChange, 
  onClick 
}: SidebarApplianceInfoProps) {
  // Group specs by specGroup
  const groupedSpecs = appliance.modelSpecs.reduce(
    (acc, spec) => {
      if (!acc[spec.specGroup]) {
        acc[spec.specGroup] = []
      }
      acc[spec.specGroup].push(spec)
      return acc
    },
    {} as Record<string, typeof appliance.modelSpecs>,
  )

  return (
    <Collapsible
      open={isOpen}
      onOpenChange={onOpenChange}
      className={`w-full rounded-lg border border-border !bg-white text-card-foreground shadow-sm ${isActive && isOpen ? '!border-gray-600 hover:!border-gray-700' : ''}`}
    >
      <CollapsibleTrigger 
        className={`flex w-full rounded-t-md items-center px-3 py-2 text-left hover:bg-accent/50 ${isActive && isOpen ? 'bg-gray-600 text-white hover:bg-gray-700' : ''}`}
        onClick={onClick}
      >
        <div className="flex items-center w-full">
          {isOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
          <div className="ml-2 flex-1 text-sm font-medium truncate">{appliance.modelInfo.modelName}</div>
        </div>
      </CollapsibleTrigger>

      <CollapsibleContent>
          <div className="px-4 py-3">
            <div className="space-y-4">
              {/* Basic Info */}
              <div className="space-y-1 mb-0">
                <p className="text-sm text-muted-foreground"><b>모델명:</b> {appliance.modelInfo.modelSuffix}</p>
                <p className="text-sm text-muted-foreground"><b>제품 구매일:</b> {appliance.modelInfo.purchaseDate}</p>
              </div>
              <Separator className="my-2" />
              {/* Specs */}
              <div className="space-y-3">
                {Object.entries(groupedSpecs).map(([group, specs]) => (
                  <div key={group}>
                    <h4 className="text-md font-semibold border-b border-border pb-1">{group}</h4>
                    <div className="mt-1 space-y-1">
                      {specs.map((spec, index) => (
                        <div key={index} className="flex justify-between text-sm">
                          <span className="font-medium">{spec.specName}</span>
                          <span className="text-muted-foreground font-light">{spec.specValue}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
              <Separator className="my-2" />
              {/* Features */}
              <div>
                <h4 className="text-md font-semibold border-b border-border pb-1 mb-2">부가 기능</h4>
                <div className="flex flex-wrap gap-1">
                  {appliance.modelFeatures.map((feature, index) => (
                    <Badge key={index} className="!bg-gray-400 text-white font-medium text-sm px-2 py-0 h-5">
                      {feature.featureName}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          </div>
      </CollapsibleContent>
    </Collapsible>
  )
}
